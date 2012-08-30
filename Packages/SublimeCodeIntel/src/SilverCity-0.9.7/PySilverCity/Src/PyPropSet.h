// Copyright 2002 by Brian Quinlan <brian@sweetapp.com>
// The License.txt file describes the conditions under which this 
// software may be distributed.

#ifndef PYPROPSET_H_
#define PYPROPSET_H_

#include <Python.h>

#include <PropSetSimple.h>

extern PyTypeObject PyPropSetType;

typedef struct {
    PyObject_HEAD
    PropSetSimple * propSet;
} PyPropSet;

#define PyPropSet_Check(op) ((op)->ob_type == &PyPropSetType)
#define PyPropSet_GET_PROPSET(op) (((PyPropSet *)(op))->propSet)

PyObject*
PyPropSet_new(PyObject *, PyObject* args);

void
initPyPropSet(void);

#endif // PYPROPSET_H_