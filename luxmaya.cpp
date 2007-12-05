// Main LUXMaya Loader
// Mark Colbert
// Dom COCO

#include "luxexport.h"
#include "launchlux.h"
#include "luxview.h"

#include <maya/MObject.h>
#include <maya/MGlobal.h>
#include <maya/MFnPlugin.h>


MStatus initializePlugin( MObject obj )
{ 
	MStatus status;

	// load the plugins
	MFnPlugin plugin ( obj, "Mark Colbert, Dom COCO", "8.5", "Any" );
	status = plugin.registerCommand( "luxexport", lux::Export::creator );
	if ( !status )
		status.perror("registerCommand");

	status = plugin.registerCommand( "luxview", LUXView::creator );
	if ( !status )
		status.perror("registerCommand");

	status = plugin.registerCommand( "launchlux", LaunchLUX::creator );
	if ( !status )
		status.perror("registerCommand");

	// create the renderer
	MGlobal::executeCommand("global proc luxRender(int $width, int $height, string $doShadows, string $arg4, string $cameraname, string $layerargs ) { "
							"	string $location = `workspace -q -rd`;							"
							"	string $fName[] = `file -q -l`; string $buffer[]; string $buffer2[]; $numTokens = `tokenize $fName[0] \"/\" $buffer`; string $fShortName = `tokenize $buffer[size($buffer)-1] \".\" $buffer2`;	"
							"	string $output = $location + \"/\" + $buffer2[0] + \".lxs\";	"
							"	string $tga = $location + \"/\" + $buffer2[0] + \".tga\";		"
							"	luxexport $output $tga $width $height $cameraname;			"
							"	launchlux ($output);										"
							"	luxview $tga;												"
							"}																"
							"renderer -rendererUIName \"LUX Renderer\"						"
							"		  -renderProcedure \"luxRender\"						"
							"		   lux;												");


	MGlobal::executeCommand("renderer -edit -addGlobalsTab \"Common\" \"createMayaSoftwareCommonGlobalsTab\" \"updateMayaSoftwareCommonGlobalsTab\" lux;");

	return status;
}

MStatus uninitializePlugin( MObject obj )
{
	MStatus status;

	MFnPlugin plugin( obj );
	status = plugin.deregisterCommand( "luxexport" );
	if ( ! status )
		status.perror("deregisterCommand");

	status = plugin.deregisterCommand( "luxview" );
	if ( ! status )
		status.perror("deregisterCommand");

	status = plugin.deregisterCommand( "launchlux" );
	if ( ! status )
		status.perror("deregisterCommand");

	MGlobal::executeCommand("renderer -unregisterRenderer lux;");

	return status;
}