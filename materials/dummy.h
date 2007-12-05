/*
 *  dummy.h
 *  luxmaya
 *
 *  Created by Mark Colbert on 10/16/04.
 *  Copyright 2004 __MyCompanyName__. All rights reserved.
 *
 */

#ifndef _LUX_DUMMY_MATERIAL_H
#define _LUX_DUMMY_MATERIAL_H

#include "material.h"

namespace lux {
	class Dummy: public Material {
		public:
			Dummy(MFnDependencyNode &_shaderNode) : Material(_shaderNode) {}
			~Dummy() {}

		protected:
			void Insert(std::ostream& fout) const;

	};
}

#endif
