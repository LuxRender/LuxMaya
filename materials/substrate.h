/*
 *  substrate.h
 *  luxmaya
 *
 *  Created by Mark Colbert on 12/5/04.
 *  Copyright 2004 __MyCompanyName__. All rights reserved.
 *
 */

#ifndef _LUX_SUBSTRATE_MATERIAL_H
#define _LUX_SUBSTRATE_MATERIAL_H

#include "material.h"

namespace lux {
	class Substrate: public Material {
		public:
			Substrate(MFnDependencyNode &_shaderNode) : Material(_shaderNode) {}
			~Substrate() {}

		protected:
			void Insert(std::ostream& fout) const;

	};
}

#endif
