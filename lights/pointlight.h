/*
 *  pointlight.h
 *  luxmaya
 *
 *  Created by Mark Colbert on 10/9/04.
 *  Copyright 2004 __MyCompanyName__. All rights reserved.
 *
 */

#ifndef _LUXPOINTLIGHT_H
#define _LUXPOINTLIGHT_H

#include <maya/MFnPointLight.h>

#include "light.h"

namespace lux {
	
	class PointLight : public Light {
		public:
			PointLight(const MDagPath &dagPath) : Light(dagPath), light(dagPath) {}
			~PointLight() {}
						
		protected:
			void Insert(std::ostream& fout) const;
			MFnPointLight light;
	};

}

#endif
