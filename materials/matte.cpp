/*
 *  Plastic.cpp
 *  luxmaya
 *
 *  Created by Mark Colbert on 10/16/04.
 *  Copyright 2004 __MyCompanyName__. All rights reserved.
 *
 */

#include "matte.h"

namespace lux {
	void Matte::Insert(std::ostream& fout) const {
		int texcolor=0, texbump=0;

		texcolor = colorTexture(fout);
		texbump = bumpTexture(fout);

		if (texcolor) {
			fout << "Material \"matte\" \"texture Kd\" \"" << texcolor << "\"";
			if (texbump) fout << " \"texture bumpmap\" \"" << texbump << "\"";
			fout << endl;
		}

	}

}
