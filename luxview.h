
#ifndef _LUX_VIEW_H
#define _LUX_VIEW_H

#include <maya/MPxCommand.h>
#include <maya/MArgList.h>
#include <maya/MStatus.h>

class LUXView: public MPxCommand
{
public:
	LUXView() {}
	virtual	~LUXView() {}
	
	static void* creator();
	virtual MStatus	doIt( const MArgList& );
};

#endif
