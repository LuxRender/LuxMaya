/*
 *  mesh.h
 *  luxmaya
 *
 *  Created by Mark Colbert on 10/7/04.
 *  Copyright 2004 University of Central Florida. All rights reserved.
 *
 */

#ifndef __LUXMESH_H
#define __LUXMESH_H

#include "object.h"
#include "polygonset.h"
#include <vector>

#include <maya/MDagPath.h>

namespace lux {
	class Mesh : public Object {
		public:
			Mesh(const MDagPath &dagPath);
			~Mesh();
			
			void SetMesh(const MDagPath &dagPath);
			void Insert(std::ostream& fout) const;
		private:
			MStatus Mesh::TranslationMatrix(ostream& fout) const;
			std::vector<PolygonSet> polySets;
			MDagPath dagPath;
	};
	
}

#endif
