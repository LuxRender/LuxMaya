/*
 *  uber.h
 *  luxmaya
 *
 *  Created by Mark Colbert on 12/5/04.
 *  Copyright 2004 __MyCompanyName__. All rights reserved.
 *
 */

#ifndef _LUX_UBER_MATERIAL_H
#define _LUX_UBER_MATERIAL_H

#include "material.h"

namespace lux {
	class Uber: public Material {
		public:
			Uber(MFnDependencyNode &_shaderNode) : Material(_shaderNode) {}
			~Uber() {}

		protected:
			void Insert(std::ostream& fout) const;

	};
}

#endif
