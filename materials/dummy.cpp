/*
 *  dummy.cpp
 *  luxmaya
 *
 *  Created by Mark Colbert on 10/16/04.
 *  Copyright 2004 __MyCompanyName__. All rights reserved.
 *
 */

#include "dummy.h"

namespace lux {
	void Dummy::Insert(std::ostream& fout) const {
		int texcolor=0, texbump=0;

		texcolor = colorTexture(fout);
		texbump = bumpTexture(fout);

		if (texcolor) {
			fout << "Material \"carpaint\" \"string name\" [\"bmw339\"]";
			if (texbump) fout << " \"texture bumpmap\" \"" << texbump << "\"";
			fout << endl;
		}

	}

}
