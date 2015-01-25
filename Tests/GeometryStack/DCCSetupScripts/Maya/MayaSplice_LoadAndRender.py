
import json
from maya import cmds

import os
if 'FABRIC_RIGGINGTOOLBOX_PATH' not in os.environ:
  raise Exception("Please set the rigging ")
toolboxPath = os.environ['FABRIC_RIGGINGTOOLBOX_PATH']

cmds.file(new=True,f=True)
cmds.file(toolboxPath+"/Tests/GeometryStack/Resources/SkinnedTube_hierarchy.ma", r=True);


##############################################
## Set up the loader node.

initnode = cmds.createNode("spliceMayaNode", name = "tubeCharacter_Init")

cmds.fabricSplice('addInputPort', initnode, json.dumps({'portName':'filePath', 'dataType':'String', 'addMayaAttr': True}))
cmds.fabricSplice('addOutputPort', initnode, json.dumps({'portName':'stack', 'dataType':'GeometryStack', 'extension':'RiggingToolbox', 'addSpliceMayaAttr':True, 'autoInitObjects': True}))

cmds.setAttr(initnode + '.filePath', toolboxPath+"/Tests/GeometryStack/Resources/tubeCharacter_Skinning.json", type="string");


cmds.fabricSplice('addKLOperator', initnode, '{"opName":"tubeCharacter_Init"}', """

require RiggingToolbox;

inline __compile_Vec3Attribute_copyFrom() { Vec3 a[]; Vec3 b[]; Vec3Attribute_copyFrom<<<1@true>>>(a, b); }
inline __compile_SkinningAttribute_copyFrom() { SkinningAttributeData a; SkinningAttributeData b; SkinningAttribute_copyFrom<<<1@true>>>(a, b); }
inline __compile_skinningModifier_skinMeshPositions() { 
  PolygonMeshTopology a; Vec3 b[]; SkinningAttributeData d; Mat44 e[]; skinningModifier_skinMeshPositions<<<1@true>>>(a, b, d, e); 
}
inline __compile_skinningModifier_skinMeshPositionsAndNormals() { 
  PolygonMeshTopology a; Vec3 b[]; Vec3 c[]; SkinningAttributeData d; Mat44 e[]; skinningModifier_skinMeshPositionsAndNormals<<<1@true>>>(a, b, c, d, e); 
}

operator tubeCharacter_Init(
  String filePath,
  io GeometryStack stack
) {
  report("Loading Character Definition:" + filePath);
  stack.loadJSONFile(filePath);

  stack.setDisplayGeometries(displayGeometries);

  //StartFabricProfiling();

  stack.evaluate(context);

  // Uncomment these lines to get a profiling report. 
  //StopFabricProfiling();
  //report( GetEvalPathReport() );
  //report(stack.getDesc());

}
""")
  

##############################################
## Set up the eval locator.

forceEvalLocator = cmds.createNode("locator", name = "forceEval")
cmds.connectAttr(evalStackNode + '.eval', forceEvalLocator + '.localPosition.localPositionY')
