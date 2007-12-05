/*
 *  arealight.cpp
 *  luxmaya
 *
 *  Created by Mark Colbert on 10/16/04.
 *  Copyright 2004 __MyCompanyName__. All rights reserved.
 *
 */

#include "arealight.h"

#include <Maya/MPlug.h>
#include <Maya/MGlobal.h>
#include <Maya/MFnNumericData.h>

namespace lux {
	void AreaLight::Insert(std::ostream& fout) const {

			MStatus status;
			MObject object;

			MPlug outColorPlug = MFnDependencyNode(shaderNode).findPlug("outColor");
			status = outColorPlug.getValue(object);
			if (status != MStatus::kSuccess) { MGlobal::displayWarning("Could not get color value out"); }

			MFnNumericData outColorData(object, &status);
			if (status != MStatus::kSuccess) { MGlobal::displayWarning("Could not get color data"); }

			fout << "AreaLightSource \"area\" \"integer nsamples\" [4] ";
			if (outColorData.numericType() == MFnNumericData::k3Float) {
				float r,g,b;
				outColorData.getData(r,g,b);
				fout << "\"color L\" [" << r << " " << g << " " << b << "] ";

			} else if (outColorData.numericType() == MFnNumericData::k3Double) {
				double r,g,b;
				outColorData.getData(r,g,b);
				fout << "\"color L\" [" << r << " " << g << " " << b << "] ";
			}
			fout << endl;
	}
}
