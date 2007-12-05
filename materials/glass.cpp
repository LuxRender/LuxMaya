/*
 *  glass.cpp
 *  luxmaya
 *
 *  Created by Mark Colbert on 12/5/04.
 *  Copyright 2004 __MyCompanyName__. All rights reserved.
 *
 */

#include "glass.h"

#include <Maya/MPlug.h>
#include <Maya/MGlobal.h>
#include <Maya/MFnNumericData.h>

namespace lux {
	void Glass::Insert(std::ostream& fout) const {
		int texcolor=0, texbump=0;

		texcolor = colorTexture(fout);
		texbump = bumpTexture(fout);

		MStatus status;
		MObject object;

		MPlug transparencyPlug = MFnDependencyNode(shaderNode).findPlug("transparency");
		MPlug specularPlug = MFnDependencyNode(shaderNode).findPlug("specularColor");
		MPlug refractiveIndexPlug = MFnDependencyNode(shaderNode).findPlug("refractiveIndex");
		status = specularPlug.getValue(object);
		if (status != MStatus::kSuccess) { MGlobal::displayWarning("Could not get specular color value out"); }

		MFnNumericData specularData(object, &status);
		if (status != MStatus::kSuccess) { MGlobal::displayWarning("Could not get specular color data"); }



		if (texcolor) {
			fout << "Material \"glass\" \"texture Kt\" \"" << texcolor << "\" ";
			if (texbump) fout << "\"texture bumpmap\" \"" << texbump << "\" ";

			if (specularData.numericType() == MFnNumericData::k3Float) {
				float r,g,b;
				specularData.getData(r,g,b);
				fout << "\"color Kr\" [" << r << " " << g << " " << b << "] ";

			} else if (specularData.numericType() == MFnNumericData::k3Double) {
				double r,g,b;
				specularData.getData(r,g,b);
				fout << "\"color Kr\" [" << r << " " << g << " " << b << "] ";
			}
			/*
			float uroughness;
			status = eccentricityPlug.getValue(uroughness);
			if (status == MStatus::kSuccess) fout << "\"float uroughness\" [" << uroughness  << "] ";

			float vroughness;
			status = specularRollOffPlug.getValue(vroughness);
			if (status == MStatus::kSuccess) fout << "\"float vroughness\" [" << vroughness  << "] ";
			*/
			float index;
			status = refractiveIndexPlug.getValue(index);
			if (status == MStatus::kSuccess) fout << "\"float index\" [" << index  << "] ";

			fout << endl;
		}

	}

}
