/*
 *  object.h
 *  luxmaya
 *
 *  Created by Mark Colbert on 10/5/04.
 *  Copyright 2004 __MyCompanyName__. All rights reserved.
 *
 */

#ifndef _LUXOBJECT_H
#define _LUXOBJECT_H

#include <iostream>

namespace lux {
	
	class Object {
		public:
			Object() {}
			virtual ~Object() {}
			
			// overload the insertion operator for easy output of the objects
			friend std::ostream& operator<<(std::ostream& fout, const Object &object);
			
		protected:
			virtual void Insert(std::ostream& fout) const = 0;
			
	};

}

#endif
