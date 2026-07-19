#define PY_SSIZE_T_CLEAN
#define NO_IMPORT_ARRAY
#define PY_ARRAY_UNIQUE_SYMBOL FPC_ARRAY_API
#include <Python.h>
#include <numpy/arrayobject.h>
#include <math.h>
#include <stdint.h>
#include <stdbool.h>

#include "methods.h"


typedef enum {
    PF_INT8    = 1,
    PF_UINT8   = 2,
    PF_INT16   = 3,
    PF_UINT16  = 4,
    PF_INT32   = 5,
    PF_UINT32  = 6,
    PF_FLOAT32 = 7,
    PF_FLOAT64 = 8
} PointFieldType;


static int host_little_endian(void) {
    uint16_t x = 1;
    return *((uint8_t*)&x);
}



// AOT Decode conversions

#define BSWAP_int8_t(v) (v)
#define BSWAP_uint8_t(v) (v)
#define BSWAP_int16_t(v) ((int16_t)__builtin_bswap16((uint16_t)(v)))
#define BSWAP_uint16_t(v) (__builtin_bswap16(v))
#define BSWAP_int32_t(v) ((int32_t)__builtin_bswap32((uint32_t)(v)))
#define BSWAP_uint32_t(v) (__builtin_bswap32(v))
#define BSWAP_float(v) (bswap_float32(v))
#define BSWAP_double(v) (bswap_float64(v))

static inline float bswap_float32(float f) {
    union { uint32_t u; float f; } t;
    t.f = f;
    t.u = __builtin_bswap32(t.u);
    return t.f;
}
 
static inline double bswap_float64(double d) {
    union { uint64_t u; double f; } t;
    t.f = d;
    t.u = __builtin_bswap64(t.u);
    return t.f;
}

#define READ_VAL(T, p, SWAP) \
    ((SWAP) ? BSWAP_##T(*(const T*)(p)) : *(const T*)(p))

#define FOR_EACH_FIELD_TYPE(X) \
    X(PF_INT8, int8_t) \
    X(PF_UINT8, uint8_t) \
    X(PF_INT16, int16_t) \
    X(PF_UINT16, uint16_t) \
    X(PF_INT32, int32_t) \
    X(PF_UINT32, uint32_t) \
    X(PF_FLOAT32, float) \
    X(PF_FLOAT64, double)


typedef Py_ssize_t (*decode_fn_t)(
    const char* base, Py_ssize_t n_points, int point_step,
    int ox, int oy, int oz, int oi, bool skip_nans,
    float* restrict xyz_data, float* restrict i_data);


#define DEFINE_LOOP_NOINTEN(XPF, XT, SWAP) \
static Py_ssize_t decode_loop_##XPF##_none_s##SWAP( \
    const char* base, Py_ssize_t n_points, int point_step, \
    int ox, int oy, int oz, int oi, bool skip_nans, \
    float* restrict xyz_data, float* restrict i_data) \
{ \
    (void)oi; (void)i_data; \
    Py_ssize_t count = 0; \
    const char* p = base; \
    for (Py_ssize_t idx = 0; idx < n_points; idx++, p += point_step) { \
        float x = (float)READ_VAL(XT, p + ox, SWAP); \
        float y = (float)READ_VAL(XT, p + oy, SWAP); \
        float z = (float)READ_VAL(XT, p + oz, SWAP); \
        \
        if (skip_nans && (isnan(x) || isnan(y) || isnan(z))) { \
            continue; \
        } \
        \
        xyz_data[count * 3 + 0] = x; \
        xyz_data[count * 3 + 1] = y; \
        xyz_data[count * 3 + 2] = z; \
        count++; \
    } \
    return count; \
}

#define DEFINE_LOOP_NOINTEN_BOTH_SWAPS(XPF, XT) \
    DEFINE_LOOP_NOINTEN(XPF, XT, 0) \
    DEFINE_LOOP_NOINTEN(XPF, XT, 1)
 
FOR_EACH_FIELD_TYPE(DEFINE_LOOP_NOINTEN_BOTH_SWAPS)


#define DEFINE_LOOP_WITHINTEN(XPF, XT, IPF, IT, SWAP) \
static Py_ssize_t decode_loop_##XPF##_##IPF##_s##SWAP( \
    const char* base, Py_ssize_t n_points, int point_step, \
    int ox, int oy, int oz, int oi, bool skip_nans, \
    float* restrict xyz_data, float* restrict i_data) \
{ \
    Py_ssize_t count = 0; \
    const char* p = base; \
    for (Py_ssize_t idx = 0; idx < n_points; idx++, p += point_step) { \
        float x = (float)READ_VAL(XT, p + ox, SWAP); \
        float y = (float)READ_VAL(XT, p + oy, SWAP); \
        float z = (float)READ_VAL(XT, p + oz, SWAP); \
        float inten = (float)READ_VAL(IT, p + oi, SWAP); \
        \
        if (skip_nans && (isnan(x) || isnan(y) || isnan(z) || isnan(inten))) { \
            continue; \
        } \
        \
        xyz_data[count * 3 + 0] = x; \
        xyz_data[count * 3 + 1] = y; \
        xyz_data[count * 3 + 2] = z; \
        i_data[count] = inten; \
        count++; \
    } \
    return count; \
}

#define DEFINE_LOOP_WITHINTEN_BOTH_SWAPS(XPF, XT, IPF, IT) \
    DEFINE_LOOP_WITHINTEN(XPF, XT, IPF, IT, 0) \
    DEFINE_LOOP_WITHINTEN(XPF, XT, IPF, IT, 1)
 
#define DEFINE_ALL_WITHINTEN_FOR_XYZ(XPF, XT) \
    DEFINE_LOOP_WITHINTEN_BOTH_SWAPS(XPF, XT, PF_INT8,    int8_t)  \
    DEFINE_LOOP_WITHINTEN_BOTH_SWAPS(XPF, XT, PF_UINT8,   uint8_t) \
    DEFINE_LOOP_WITHINTEN_BOTH_SWAPS(XPF, XT, PF_INT16,   int16_t) \
    DEFINE_LOOP_WITHINTEN_BOTH_SWAPS(XPF, XT, PF_UINT16,  uint16_t) \
    DEFINE_LOOP_WITHINTEN_BOTH_SWAPS(XPF, XT, PF_INT32,   int32_t) \
    DEFINE_LOOP_WITHINTEN_BOTH_SWAPS(XPF, XT, PF_UINT32,  uint32_t) \
    DEFINE_LOOP_WITHINTEN_BOTH_SWAPS(XPF, XT, PF_FLOAT32, float)   \
    DEFINE_LOOP_WITHINTEN_BOTH_SWAPS(XPF, XT, PF_FLOAT64, double)
 
FOR_EACH_FIELD_TYPE(DEFINE_ALL_WITHINTEN_FOR_XYZ)
  
#define CASE_XYZ_NO_INTEN(XPF, XT) \
    case XPF: return swap ? decode_loop_##XPF##_none_s1 : decode_loop_##XPF##_none_s0;
 
#define CASE_WITHINTEN_INNER(XPF, XT, IPF, IT) \
        case IPF: return swap ? decode_loop_##XPF##_##IPF##_s1 : decode_loop_##XPF##_##IPF##_s0;
 
#define GEN_INTEN_CASES(XPF, XT) \
    CASE_WITHINTEN_INNER(XPF, XT, PF_INT8,    int8_t)  \
    CASE_WITHINTEN_INNER(XPF, XT, PF_UINT8,   uint8_t) \
    CASE_WITHINTEN_INNER(XPF, XT, PF_INT16,   int16_t) \
    CASE_WITHINTEN_INNER(XPF, XT, PF_UINT16,  uint16_t) \
    CASE_WITHINTEN_INNER(XPF, XT, PF_INT32,   int32_t) \
    CASE_WITHINTEN_INNER(XPF, XT, PF_UINT32,  uint32_t) \
    CASE_WITHINTEN_INNER(XPF, XT, PF_FLOAT32, float)   \
    CASE_WITHINTEN_INNER(XPF, XT, PF_FLOAT64, double)
 
#define CASE_XYZ_WITH_INTEN(XPF, XT) \
    case XPF: switch (dtype_intensity) { \
        GEN_INTEN_CASES(XPF, XT) \
        default: return NULL; \
    }
 
static decode_fn_t select_decode_fn(PointFieldType dtype_xyz, bool has_intensity, PointFieldType dtype_intensity, int swap) {
    if (!has_intensity) {
        switch (dtype_xyz) {
            FOR_EACH_FIELD_TYPE(CASE_XYZ_NO_INTEN)
            default: return NULL;
        }
    } else {
        switch (dtype_xyz) {
            FOR_EACH_FIELD_TYPE(CASE_XYZ_WITH_INTEN)
            default: return NULL;
        }
    }
}
 
#undef CASE_XYZ_WITH_INTEN
#undef GEN_INTEN_CASES
#undef CASE_WITHINTEN_INNER
#undef CASE_XYZ_NO_INTEN
#undef DEFINE_ALL_WITHINTEN_FOR_XYZ
#undef DEFINE_LOOP_WITHINTEN_BOTH_SWAPS
#undef DEFINE_LOOP_WITHINTEN
#undef DEFINE_LOOP_NOINTEN_BOTH_SWAPS
#undef DEFINE_LOOP_NOINTEN
#undef FOR_EACH_FIELD_TYPE
#undef READ_VAL
#undef BSWAP_int8_t
#undef BSWAP_uint8_t
#undef BSWAP_int16_t
#undef BSWAP_uint16_t
#undef BSWAP_int32_t
#undef BSWAP_uint32_t
#undef BSWAP_float
#undef BSWAP_double


// End of AOT decode selection


static PyObject* build_empty_ret(bool has_intensity) {
    PyObject* xyz = PyArray_SimpleNew(2, ((npy_intp[]){0, 3}), NPY_FLOAT32);
    if (!xyz) return NULL;

    PyObject* intensity = Py_None;
    if (has_intensity) {
        intensity = PyArray_SimpleNew(1, (npy_intp[]){0}, NPY_FLOAT32);
        if (!intensity) {
            Py_DECREF(xyz);
            return NULL;
        }
    } else {
        Py_INCREF(Py_None);
    }

    PyObject* ret = PyTuple_Pack(2, xyz, intensity);
    Py_DECREF(xyz);
    Py_DECREF(intensity);

    return ret;
}



// unused attr to prevent compiler from giving that dumb warning
__attribute__((unused)) PyObject* decode_xyz_intensity(PyObject* self, PyObject* args) {
    PyObject* data_obj;
    int point_step, ox, oy, oz, oi;
    int is_bigendian, dtype_xyz_val, dtype_intensity_val, skip_nans;

    if (!PyArg_ParseTuple(args, "Oiiiiiiiii", 
            &data_obj, &point_step, &ox, &oy, &oz, &oi,
            &is_bigendian, &dtype_xyz_val, &dtype_intensity_val, &skip_nans)) {
        return NULL;
    }

    PointFieldType dtype_xyz = (PointFieldType)dtype_xyz_val;
    PointFieldType dtype_intensity = (PointFieldType)dtype_intensity_val;
    bool has_intensity = (oi >= 0);
    
    // https://users.pja.edu.pl/~error501/python-html/c-api/buffer.html
    Py_buffer buf;
    if (PyObject_GetBuffer(data_obj, &buf, PyBUF_SIMPLE) != 0) {
        return NULL;
    }

    if (buf.len == 0 || point_step <= 0) {
        PyBuffer_Release(&buf);
        return build_empty_ret(oi >= 0);
    }

    Py_ssize_t n_points = buf.len / point_step;
    char* base = (char*)buf.buf;
    int swap = (host_little_endian() == is_bigendian);

    decode_fn_t fn = select_decode_fn(dtype_xyz, has_intensity, dtype_intensity, swap);

    // why we do this: https://docs.python.org/3/extending/extending.html#back-to-the-example
    // about ref counts: // https://docs.python.org/3/extending/extending.html#reference-counts
    PyObject* xyz = PyArray_SimpleNew(2, ((npy_intp[]){n_points, 3}), NPY_FLOAT32);
    PyObject* intensity = (oi >= 0) ? PyArray_SimpleNew(1, ((npy_intp[]){n_points}), NPY_FLOAT32) : Py_None;
    if (intensity == Py_None) Py_INCREF(Py_None);

    
    float* restrict xyz_data = (float*)PyArray_DATA((PyArrayObject*)xyz);
    float* restrict i_data = (oi >= 0) ? (float*)PyArray_DATA((PyArrayObject*)intensity) : NULL;

    Py_ssize_t count;
    Py_BEGIN_ALLOW_THREADS
    count = fn(base, n_points, point_step, ox, oy, oz, oi, (bool)skip_nans, xyz_data, i_data);
    Py_END_ALLOW_THREADS

    PyBuffer_Release(&buf);

    if (count != n_points) {
        PyArray_Dims newshape = {(npy_intp[]){count, 3}, 2};
        PyArray_Resize((PyArrayObject*)xyz, &newshape, 1, NPY_CORDER);

        if (i_data) {
            PyArray_Dims newshape_i = {(npy_intp[]){count}, 1};
            PyArray_Resize((PyArrayObject*)intensity, &newshape_i, 1, NPY_CORDER);
        }
    }

    PyObject* ret = PyTuple_Pack(2, xyz, intensity);
    Py_DECREF(xyz); // i hope this ref tracking is correct
    Py_DECREF(intensity);

    return ret;
}
