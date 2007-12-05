/*
 *  spotlight.h
 *  luxmaya
 *
 *  Created by Mark Colbert on 10/9/04.
 *  Copyright 2004 __MyCompanyName__. All rights reserved.
 *
 */

#ifndef _LUXSPOTLIGHT_H
#define _LUXSPOTLIGHT_H

#include <maya/MFnSpotLight.h>

#include "light.h"

namespace lux {
	
	class SpotLight : public Light {
		public:
			SpotLight(const MDagPath &dagPath) : Light(dagPath), light(dagPath) {}
			~SpotLight() {}
						
		protected:
			void Insert(std::ostream& fout) const;
			MFnSpotLight light;
	};

}

#endif
