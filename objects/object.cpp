/*
 *  object.cpp
 *  luxmaya
 *
 *  Created by Mark Colbert on 10/5/04.
 *
 */

#include "object.h"

using namespace std;

namespace lux {
	
	ostream& operator<< (ostream& fout, const Object& obj) {
		obj.Insert(fout);
		return fout;
	}

}
