/*
 *  shinymetal.h
 *  luxmaya
 *
 *  Created by Mark Colbert on 10/11/04.
 *  Copyright 2004 __MyCompanyName__. All rights reserved.
 *
 */

#ifndef _LUX_SHINY_METAL_MATERIAL_H
#define _LUX_SHINY_METAL_MATERIAL_H

#include "material.h"

namespace lux {
	class ShinyMetal: public Material {
		public:
			ShinyMetal(MFnDependencyNode &_shaderNode) : Material(_shaderNode) {}
			~ShinyMetal() {}

		protected:
			void Insert(std::ostream& fout) const;

	};
}

#endif

