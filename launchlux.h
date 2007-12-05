
#ifndef _LAUNCH_LUX_H
#define _LAUNCH_LUX_H

#include <maya/MPxCommand.h>
#include <maya/MArgList.h>
#include <maya/MStatus.h>


class LaunchLUX: public MPxCommand
{
public:
	LaunchLUX() {}
	virtual	~LaunchLUX() {}
	
	static void* creator();
	virtual MStatus	doIt( const MArgList& );
};

#endif
