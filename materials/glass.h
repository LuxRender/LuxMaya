/*
 *  glass.h
 *  luxmaya
 *
 *  Created by Mark Colbert on 10/16/04.
 *  Copyright 2004 __MyCompanyName__. All rights reserved.
 *
 */

#ifndef _LUX_GLASS_MATERIAL_H
#define _LUX_GLASS_MATERIAL_H

#include "material.h"

namespace lux {
	class Glass: public Material {
		public:
			Glass(MFnDependencyNode &_shaderNode) : Material(_shaderNode) {}
			~Glass() {}

		protected:
			void Insert(std::ostream& fout) const;

	};
}

#endif
