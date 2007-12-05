/*
 *  Plastic.h
 *  luxmaya
 *
 *  Created by Mark Colbert on 10/16/04.
 *  Copyright 2004 __MyCompanyName__. All rights reserved.
 *
 */

#ifndef _LUX_MATTE_MATERIAL_H
#define _LUX_MATTE_MATERIAL_H

#include "material.h"

namespace lux {
	class Matte: public Material {
		public:
			Matte(MFnDependencyNode &_shaderNode) : Material(_shaderNode) {}
			~Matte() {}

		protected:
			void Insert(std::ostream& fout) const;

	};
}

#endif
