/*
 *  arealight.h
 *  luxmaya
 *
 *  Created by Mark Colbert on 10/16/04.
 *  Copyright 2004 __MyCompanyName__. All rights reserved.
 *
 */

#ifndef _LUX_AREALIGHT_MATERIAL_H
#define _LUX_AREALIGHT_MATERIAL_H

#include "material.h"

namespace lux {
	class AreaLight: public Material {
		public:
			AreaLight(MFnDependencyNode &_shaderNode) : Material(_shaderNode) {}
			~AreaLight() {}

		protected:
			void Insert(std::ostream& fout) const;

	};
}

#endif
