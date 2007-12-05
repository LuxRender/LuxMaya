/*
 *  luxexport.h
 *  luxmaya
 *
 *  Created by Mark Colbert on 10/5/04.
 *  Copyright 2004 University of Central Florida. All rights reserved.
 *
 */

#ifndef _LUXEXPORTER_H
#define _LUXEXPORTER_H

#include <maya/MPxCommand.h>
#include <maya/MArgList.h>
#include <maya/MFnDagNode.h>

namespace lux {

	class Export: public MPxCommand
	{
	public:
		Export() {}
		virtual	~Export() {}
		static void* creator();
		virtual MStatus	doIt( const MArgList& );

	private:
		bool			isVisible(MFnDagNode & fnDag, MStatus *status = NULL);
	};

}

#endif

