// Scintilla source code edit control
/** @file PropSetSimple.h
 ** A basic string to string map.
 **/
// Copyright 1998-2009 by Neil Hodgson <neilh@scintilla.org>
// The License.txt file describes the conditions under which this software may be distributed.

#ifndef PROPSETSIMPLE_H
#define PROPSETSIMPLE_H

#include "PropSet.h"
#include <map>
#include <string>

#ifdef SCI_NAMESPACE
namespace Scintilla {
#endif

typedef std::map<std::string, std::string> mapss;

class PropSetSimple : public PropertyGet {
	void Set(const char *keyVal);
public:
	void *impl;
	PropSetSimple();
	virtual ~PropSetSimple();
	void Set(const char *key, const char *val, int lenKey=-1, int lenVal=-1);
	void SetMultiple(const char *);
	const char *Get(const char *key) const;
	char *Expanded(const char *key) const;
	char *ToString() const;
	int GetInt(const char *key, int defaultValue=0) const;
};

#ifdef SCI_NAMESPACE
}
#endif

#endif
