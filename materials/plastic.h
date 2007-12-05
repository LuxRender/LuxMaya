/*
 *  Plastic.h
 *  luxmaya
 *
 *  Created by Mark Colbert on 10/16/04.
 *  Copyright 2004 __MyCompanyName__. All rights reserved.
 *
 */

#ifndef _LUX_PLASTIC_MATERIAL_H
#define _LUX_PLASTIC_MATERIAL_H

#include "material.h"

namespace lux {
	class Plastic: public Material {
		public:
			Plastic(MFnDependencyNode &_shaderNode) : Material(_shaderNode) {}
			~Plastic() {}

		protected:
			void Insert(std::ostream& fout) const;

	};
}

#endif
