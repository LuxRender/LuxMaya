Name "LuxMaya"
Caption "LuxMaya Installer"
OutFile "Setup-LuxMaya.exe"
XPStyle on
CRCCheck on

; disabled due to incompatibility with dev server
; RequestExecutionLevel user

Page license
Page components
Page directory "" "" verifyLux
Page instfiles

Var MAYAVERSION

LicenseData ..\src\LICENSE.txt
ComponentText "Please select the versions of Maya that you have installed on this machine. Click Next to continue." "" "Select your Maya versions:"
DirText "Please choose the directory where you have installed Lux Renderer:" "Lux Renderer Location" "" "Location of Lux Renderer:"

Function verifyLux
 IfFileExists $INSTDIR\luxrender.exe I1Good
  MessageBox MB_OK|MB_ICONEXCLAMATION "Lux executable not found. I will still install, but some exporter options may not work." 
  ; Abort
 I1Good:
 IfFileExists $INSTDIR\luxconsole.exe I2Good
  MessageBox MB_OK|MB_ICONEXCLAMATION "Lux console executable not found. I will still install, but some exporter options may not work." 
  ; Abort
 I2Good:
FunctionEnd

; FROM HERE ON IN, $INSTDIR CONTAINS LUX'S DIRECTORY, NOT THE SCRIPT INSTALL DIRECTORY


Section /o "8.5"
 StrCpy $MAYAVERSION "8.5"
 ; LUX_SEARCHPATH
 Call insertLSP
 ; scripts
 Call copyScripts
 ; Icons
 Call copyIcons
 ; attrPresets
 Call copyPresets
 ; plugin
 Call copyPlugin
SectionEnd

Section /o "8.5 64bit"
 StrCpy $MAYAVERSION "8.5-x64"
 ; LUX_SEARCHPATH
 Call insertLSP
 ; scripts
 Call copyScripts
 ; Icons
 Call copyIcons
 ; attrPresets
 Call copyPresets
 ; plugin
 Call copyPlugin
SectionEnd

Section /o "2008"
 StrCpy $MAYAVERSION "2008"
 ; LUX_SEARCHPATH
 Call insertLSP
 ; scripts
 Call copyScripts
 ; Icons
 Call copyIcons
 ; attrPresets
 Call copyPresets
 ; plugin
 Call copyPlugin
SectionEnd

Section /o "2008 64bit"
 StrCpy $MAYAVERSION "2008-x64"
 ; LUX_SEARCHPATH
 Call insertLSP
 ; scripts
 Call copyScripts
 ; Icons
 Call copyIcons
 ; attrPresets
 Call copyPresets
 ; plugin
 Call copyPlugin
SectionEnd


Function insertLSP

 ; now update MAYA_SCRIPT_PATH in Maya.env
 Push $DOCUMENTS\maya\$MAYAVERSION\Maya.env
 Push LUX_SEARCHPATH
  Call FileSearch
 Pop $0
 Pop $1
 
 StrCmp $0 0 +2
 	Return ; string was found, do nothing
 	
 Call doInsertLSP ; string not found, insert path

FunctionEnd

Function doInsertLSP
 FileOpen $0 $DOCUMENTS\maya\$MAYAVERSION\Maya.env a
 FileSeek $0 0 END
 FileWrite $0 "$\r$\n"
 FileWrite $0 "LUX_SEARCHPATH = $INSTDIR"
 FileWrite $0 "$\r$\n"
 FileClose $0
FunctionEnd

Function copyScripts
 SetOutPath $DOCUMENTS\maya\$MAYAVERSION\scripts\LuxMaya
 File "..\src\Mel\*.mel"
 
 ; now update MAYA_SCRIPT_PATH in Maya.env
 Push $DOCUMENTS\maya\$MAYAVERSION\Maya.env
 Push MAYA_SCRIPT_PATH
  Call FileSearch
 Pop $0
 Pop $1
 
 StrCmp $0 0 +3
  Call replaceMAYA_SCRIPT_PATH	; String was found, do replace
  GoTo MSPDone
 
 Call insertMAYA_SCRIPT_PATH	; else string was not found, do an insert
 
MSPDone:

FunctionEnd

Function replaceMAYA_SCRIPT_PATH
	Push "MAYA_SCRIPT_PATH = "
	Push "MAYA_SCRIPT_PATH = $DOCUMENTS\maya\$MAYAVERSION\scripts\LuxMaya;"
	Push all
	Push all
	Push $DOCUMENTS\maya\$MAYAVERSION\Maya.env
	 Call AdvReplaceInFile
FunctionEnd

Function insertMAYA_SCRIPT_PATH
 FileOpen $0 $DOCUMENTS\maya\$MAYAVERSION\Maya.env a
 FileSeek $0 0 END
 FileWrite $0 "$\r$\n"
 FileWrite $0 "MAYA_SCRIPT_PATH = $DOCUMENTS\maya\$MAYAVERSION\scripts\LuxMaya"
 FileWrite $0 "$\r$\n"
 FileClose $0
FunctionEnd

Function copyIcons
 SetOutPath $DOCUMENTS\maya\$MAYAVERSION\scripts\LuxMaya\icons
 File "..\src\icons\*.xpm"

 ; now update XMBLANGPATH in Maya.env
 Push $DOCUMENTS\maya\$MAYAVERSION\Maya.env
 Push XBMLANGPATH
  Call FileSearch
 Pop $0
 Pop $1
 
 StrCmp $0 0 +3
  Call replaceXBMLANGPATH	; String was found, do replace
  Return
 
 Call insertXBMLANGPATH		; else string was not found, do an insert
FunctionEnd

Function replaceXBMLANGPATH
	Push "XBMLANGPATH = "
	Push "XBMLANGPATH = $DOCUMENTS\maya\$MAYAVERSION\scripts\LuxMaya\icons;"
	Push all
	Push all
	Push $DOCUMENTS\maya\$MAYAVERSION\Maya.env
	 Call AdvReplaceInFile
FunctionEnd

Function insertXBMLANGPATH
 FileOpen $0 $DOCUMENTS\maya\$MAYAVERSION\Maya.env a
 FileSeek $0 0 END
 FileWrite $0 "$\r$\n"
 FileWrite $0 "XBMLANGPATH = $DOCUMENTS\maya\$MAYAVERSION\scripts\LuxMaya\icons"
 FileWrite $0 "$\r$\n"
 FileClose $0
FunctionEnd

Function replaceMPP
	Push "MAYA_PLUG_IN_PATH = "
	Push "MAYA_PLUG_IN_PATH = $DOCUMENTS\maya\$MAYAVERSION\scripts\LuxMaya\luxPlugin;"
	Push all
	Push all
	Push $DOCUMENTS\maya\$MAYAVERSION\Maya.env
	 Call AdvReplaceInFile
FunctionEnd

Function insertMPP
 FileOpen $0 $DOCUMENTS\maya\$MAYAVERSION\Maya.env a
 FileSeek $0 0 END
 FileWrite $0 "$\r$\n"
 FileWrite $0 "MAYA_PLUG_IN_PATH = $DOCUMENTS\maya\$MAYAVERSION\scripts\LuxMaya\luxPlugin"
 FileWrite $0 "$\r$\n"
 FileClose $0
FunctionEnd

Function copyPresets
 SetOutPath $DOCUMENTS\maya\$MAYAVERSION\presets\attrPresets
 File /r /x ".svn" "..\src\attrPresets\*.*"
FunctionEnd

Function copyPlugin
 SetOutPath $DOCUMENTS\maya\$MAYAVERSION\scripts\LuxMaya\luxPlugin
 File /r "..\luxPlugin\*.py"
 
 ; look for MAYA_PLUG_IN_PATH
 Push $DOCUMENTS\maya\$MAYAVERSION\Maya.env
 Push XBMLANGPATH
  Call FileSearch
 Pop $0
 Pop $1
 
 StrCmp $0 0 +3
  Call replaceMPP	; String was found, do replace
  GoTo MPPDone
 
 Call insertMPP		; else string was not found, do an insert
 
MPPDone:
 
 ; create entry in $DOCUMENTS\maya\$MAYAVERSION\prefs\pluginPrefs.mel
 ; evalDeferred("autoLoadPlugin(\"\", \"luxPlugin.py\", \"luxPlugin\")");
 Push $DOCUMENTS\maya\$MAYAVERSION\prefs\pluginPrefs.mel
 Push "luxPlugin.py"
  Call FileSearch
 Pop $0
 Pop $1
 
 StrCmp $0 0 +3
  ; string was found, do nothing
  Return
 
 ; else string was not found, do an insert
 FileOpen $0 $DOCUMENTS\maya\$MAYAVERSION\prefs\pluginPrefs.mel a
 FileSeek $0 0 END
 FileWrite $0 "$\r$\n"
 FileWrite $0 "evalDeferred($\"autoLoadPlugin(\$\"\$\", \$\"luxPlugin.py\$\", \$\"luxPlugin\$\")$\");"
 FileWrite $0 "$\r$\n"
 FileClose $0
FunctionEnd

; http://nsis.sourceforge.net/Another_String_Replace_(and_Slash/BackSlash_Converter)
; Push $filenamestring (e.g. 'c:\this\and\that\filename.htm')
; Push "\"
; Call StrSlash
; Pop $R0
; ;Now $R0 contains 'c:/this/and/that/filename.htm'
Function StrSlash
  Exch $R3 ; $R3 = needle ("\" or "/")
  Exch
  Exch $R1 ; $R1 = String to replacement in (haystack)
  Push $R2 ; Replaced haystack
  Push $R4 ; $R4 = not $R3 ("/" or "\")
  Push $R6
  Push $R7 ; Scratch reg
  StrCpy $R2 ""
  StrLen $R6 $R1
  StrCpy $R4 "\"
  StrCmp $R3 "/" loop
  StrCpy $R4 "/"  
loop:
  StrCpy $R7 $R1 1
  StrCpy $R1 $R1 $R6 1
  StrCmp $R7 $R3 found
  StrCpy $R2 "$R2$R7"
  StrCmp $R1 "" done loop
found:
  StrCpy $R2 "$R2$R4"
  StrCmp $R1 "" done loop
done:
  StrCpy $R3 $R2
  Pop $R7
  Pop $R6
  Pop $R4
  Pop $R2
  Pop $R1
  Exch $R3
FunctionEnd

; http://nsis.sourceforge.net/Search_for_text_in_file
Function FileSearch
	Exch $R0 ;search for
	Exch
	Exch $R1 ;input file
	Push $R2
	Push $R3
	Push $R4
	Push $R5
	Push $R6
	Push $R7
	Push $R8
	Push $R9
	 
	  StrLen $R4 $R0
	  StrCpy $R7 0
	  StrCpy $R8 0
	 
	  ClearErrors
	  FileOpen $R2 $R1 r
	  IfErrors Done
	 
	  LoopRead:
	    ClearErrors
	    FileRead $R2 $R3
	    IfErrors DoneRead
	 
	    IntOp $R7 $R7 + 1
	    StrCpy $R5 -1
	    StrCpy $R9 0
	 
	    LoopParse:
	      IntOp $R5 $R5 + 1
	      StrCpy $R6 $R3 $R4 $R5
	      StrCmp $R6 "" 0 +4
	        StrCmp $R9 1 LoopRead
	          IntOp $R7 $R7 - 1
	          Goto LoopRead
	      StrCmp $R6 $R0 0 LoopParse
	        StrCpy $R9 1
	        IntOp $R8 $R8 + 1
	        Goto LoopParse
	 
	  DoneRead:
	    FileClose $R2
	  Done:
	    StrCpy $R0 $R8
	    StrCpy $R1 $R7
	 
	Pop $R9
	Pop $R8
	Pop $R7
	Pop $R6
	Pop $R5
	Pop $R4
	Pop $R3
	Pop $R2
	Exch $R1 ;number of lines found on
	Exch
	Exch $R0 ;output count found
FunctionEnd

; http://nsis.sourceforge.net/More_advanced_replace_text_in_file
Function AdvReplaceInFile
	Exch $0 ;file to replace in
	Exch
	Exch $1 ;number to replace after
	Exch
	Exch 2
	Exch $2 ;replace and onwards
	Exch 2
	Exch 3
	Exch $3 ;replace with
	Exch 3
	Exch 4
	Exch $4 ;to replace
	Exch 4
	Push $5 ;minus count
	Push $6 ;universal
	Push $7 ;end string
	Push $8 ;left string
	Push $9 ;right string
	Push $R0 ;file1
	Push $R1 ;file2
	Push $R2 ;read
	Push $R3 ;universal
	Push $R4 ;count (onwards)
	Push $R5 ;count (after)
	Push $R6 ;temp file name
	 
	  GetTempFileName $R6
	  FileOpen $R1 $0 r ;file to search in
	  FileOpen $R0 $R6 w ;temp file
	   StrLen $R3 $4
	   StrCpy $R4 -1
	   StrCpy $R5 -1
	 
	loop_read:
	 ClearErrors
	 FileRead $R1 $R2 ;read line
	 IfErrors exit
	 
	   StrCpy $5 0
	   StrCpy $7 $R2
	 
	loop_filter:
	   IntOp $5 $5 - 1
	   StrCpy $6 $7 $R3 $5 ;search
	   StrCmp $6 "" file_write2
	   StrCmp $6 $4 0 loop_filter
	 
	StrCpy $8 $7 $5 ;left part
	IntOp $6 $5 + $R3
	IntCmp $6 0 is0 not0
	is0:
	StrCpy $9 ""
	Goto done
	not0:
	StrCpy $9 $7 "" $6 ;right part
	done:
	StrCpy $7 $8$3$9 ;re-join
	 
	IntOp $R4 $R4 + 1
	StrCmp $2 all file_write1
	StrCmp $R4 $2 0 file_write2
	IntOp $R4 $R4 - 1
	 
	IntOp $R5 $R5 + 1
	StrCmp $1 all file_write1
	StrCmp $R5 $1 0 file_write1
	IntOp $R5 $R5 - 1
	Goto file_write2
	 
	file_write1:
	 FileWrite $R0 $7 ;write modified line
	Goto loop_read
	 
	file_write2:
	 FileWrite $R0 $R2 ;write unmodified line
	Goto loop_read
	 
	exit:
	  FileClose $R0
	  FileClose $R1
	 
	   SetDetailsPrint none
	  Delete $0
	  Rename $R6 $0
	  Delete $R6
	   SetDetailsPrint both
	 
	Pop $R6
	Pop $R5
	Pop $R4
	Pop $R3
	Pop $R2
	Pop $R1
	Pop $R0
	Pop $9
	Pop $8
	Pop $7
	Pop $6
	Pop $5
	Pop $0
	Pop $1
	Pop $2
	Pop $3
	Pop $4
FunctionEnd
