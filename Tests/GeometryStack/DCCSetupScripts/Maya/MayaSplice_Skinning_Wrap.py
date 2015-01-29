
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

influenceInitNode = cmds.createNode("spliceMayaNode", name = "tubeCharacter_Init")

cmds.fabricSplice('addInputPort', influenceInitNode, json.dumps({'portName':'filePath', 'dataType':'String', 'addMayaAttr': True}))
cmds.fabricSplice('addOutputPort', influenceInitNode, json.dumps({'portName':'stack', 'dataType':'GeometryStack', 'extension':'RiggingToolbox', 'addSpliceMayaAttr':True, 'autoInitObjects': True}))

cmds.setAttr(influenceInitNode + '.filePath', toolboxPath+"/Tests/GeometryStack/Resources/tubeCharacter_Skinning.json", type="string");


cmds.fabricSplice('addKLOperator', influenceInitNode, '{"opName":"tubeCharacter_Init"}', """

require RiggingToolbox;



inline __compile_Vec3Attribute_copyFrom() { Vec3 a[]; Vec3 b[]; Vec3Attribute_copyFrom<<<1@true>>>(a, b); }

// Skinning GPU Kernels
inline __compile_SkinningAttribute_copyFrom() { SkinningAttributeData a; SkinningAttributeData b; SkinningAttribute_copyFrom<<<1@true>>>(a, b); }
inline __compile_skinningModifier_skinMeshPositions() { 
  PolygonMeshTopology a; Vec3 b[]; SkinningAttributeData d; Mat44 e[]; skinningModifier_skinMeshPositions<<<1@true>>>(a,b, d, e); 
}
inline __compile_skinningModifier_skinMeshPositionsAndNormals() { 
  PolygonMeshTopology a; Vec3 b[]; Vec3 c[]; SkinningAttributeData d; Mat44 e[]; skinningModifier_skinMeshPositionsAndNormals<<<1@true>>>(a, b, c, d, e); 
}

// Compute Normals GPU Kernels
inline __compile_computeNormalsModifier_computePointNormals() { 
  PolygonMeshTopology a; Vec3 b[];Vec3 c[];Boolean d; DebugLines e; computeNormalsModifier_computePointNormals<<<1@true>>>(a, b, c, d, e); 
}

// Compute Tangents GPU Kernels
inline __compile_polygonMesh_recomputeTangents_setTangentTask() { 
  PolygonMeshTopology a; Vec4 b[];Vec4 c[]; 
  polygonMesh_recomputeTangents_setTangentTask<<<1@true>>>(a, b, c); 
}

inline __compile_polygonMesh_recomputeTangents_ComputeBiNormTask(){
  UInt32 a[];  UInt32 b[];  Vec3 c[];  Vec3 d[];  Vec3 e[];  Vec3 f[];  PolygonMeshTopology g;  Vec3 h[];  Vec2 i[];
  polygonMesh_recomputeTangents_ComputeBiNormTask<<<1@true>>>(a, b, c, d, e, f, g, h, i);
}
inline __compile_polygonMesh_recomputeTangents_computeVertexTanTask(){
  Vec4 a[];  Vec3 b[];  Vec3 c[];  Vec3 d[];
  polygonMesh_recomputeTangents_computeVertexTanTask<<<1@true>>>(a, b, c, d);
}
inline __compile_polygonMesh_recomputeTangents_countPolygonsTask(){
  PolygonMeshTopology a;  Size b; Size c; UInt32 d[]; UInt32 e[];
  polygonMesh_recomputeTangents_countPolygonsTask<<<1@true>>>(a, b, c, d, e);
}

inline __compile_deltaMushModifier_smoothPos() { PolygonMeshTopology a; Vec3 b[]; deltaMushModifier_smoothPos<<<1@true>>>(a, b); }
inline __compile_deltaMushModifier_computePointBinding() { PolygonMeshTopology a; Vec3 b[];Vec3 c[];Vec3 d[]; deltaMushModifier_computePointBinding<<<1@true>>>(a, b, c, d); }
inline __compile_deltaMushModifier_applyDeltas() { PolygonMeshTopology a; Vec3 b[];Vec3 c[];Vec3 d[]; Boolean e; DebugLines f; deltaMushModifier_applyDeltas<<<1@true>>>(a, b, c, d, e, f); }
inline __compile_deltaMushModifier_applyDeltas_Masked() { PolygonMeshTopology a; Vec3 b[];Vec3 c[];Vec3 d[]; Scalar e[]; Boolean f; DebugLines g; deltaMushModifier_applyDeltas_Masked<<<1@true>>>(a, b, c, d, e, f, g); }

inline __compile_wrapModifier_applyDeltas(){
  PolygonMeshTopology a; Vec3 b[]; Vec3 c[]; Vec4 d[]; GeometryLocation e[]; Vec3 f[]; Vec3 g[]; Vec3 h[]; Vec3 i[]; Boolean j; DebugLines k;
  wrapModifier_applyDeltas<<<1@true>>>(a,b,c,d,e,f,g,h,i,j,k);
}


operator tubeCharacter_Init(
  String filePath,
  io GeometryStack stack
) {
  report("Loading Character Definition:" + filePath);
  stack.loadJSONFile(filePath);
}
""")
  

##############################################
## Set up the skinning pose node.

influencePoseNode = cmds.createNode("spliceMayaNode", name = "tubeCharacter_Skinning")

cmds.fabricSplice('addIOPort', influencePoseNode, json.dumps({'portName':'stack', 'dataType':'GeometryStack', 'extension':'RiggingToolbox', 'addSpliceMayaAttr':True, 'autoInitObjects': False }))
cmds.fabricSplice('addInputPort', influencePoseNode, json.dumps({'portName':'displayDebugging', 'dataType':'Boolean', 'addMayaAttr': True}))
cmds.fabricSplice('addInputPort', influencePoseNode, json.dumps({'portName':'deformers', 'dataType':'Mat44[]', 'addMayaAttr': True, 'arrayType':"Array (Multi)"}))

cmds.connectAttr('SkinnedTube_hierarchy_joint1.worldMatrix[0]', influencePoseNode + '.deformers[0]')
cmds.connectAttr('SkinnedTube_hierarchy_joint2.worldMatrix[0]', influencePoseNode + '.deformers[1]')
cmds.connectAttr('SkinnedTube_hierarchy_joint3.worldMatrix[0]', influencePoseNode + '.deformers[2]')
cmds.connectAttr('SkinnedTube_hierarchy_joint4.worldMatrix[0]', influencePoseNode + '.deformers[3]')


cmds.fabricSplice('addKLOperator', influencePoseNode, '{"opName":"tubeCharacter_Skinning"}', """

require RiggingToolbox;


inline __compile_Vec3Attribute_copyFrom() { Vec3 a[]; Vec3 b[]; Vec3Attribute_copyFrom<<<1@true>>>(a, b); }

// Skinning GPU Kernels
inline __compile_SkinningAttribute_copyFrom() { SkinningAttributeData a; SkinningAttributeData b; SkinningAttribute_copyFrom<<<1@true>>>(a, b); }
inline __compile_skinningModifier_skinMeshPositions() { 
  PolygonMeshTopology a; Vec3 b[]; SkinningAttributeData d; Mat44 e[]; skinningModifier_skinMeshPositions<<<1@true>>>(a,b, d, e); 
}
inline __compile_skinningModifier_skinMeshPositionsAndNormals() { 
  PolygonMeshTopology a; Vec3 b[]; Vec3 c[]; SkinningAttributeData d; Mat44 e[]; skinningModifier_skinMeshPositionsAndNormals<<<1@true>>>(a, b, c, d, e); 
}

// Compute Normals GPU Kernels
inline __compile_computeNormalsModifier_computePointNormals() { 
  PolygonMeshTopology a; Vec3 b[];Vec3 c[];Boolean d; DebugLines e; computeNormalsModifier_computePointNormals<<<1@true>>>(a, b, c, d, e); 
}

// Compute Tangents GPU Kernels
inline __compile_polygonMesh_recomputeTangents_setTangentTask() { 
  PolygonMeshTopology a; Vec4 b[];Vec4 c[]; 
  polygonMesh_recomputeTangents_setTangentTask<<<1@true>>>(a, b, c); 
}

inline __compile_polygonMesh_recomputeTangents_ComputeBiNormTask(){
  UInt32 a[];  UInt32 b[];  Vec3 c[];  Vec3 d[];  Vec3 e[];  Vec3 f[];  PolygonMeshTopology g;  Vec3 h[];  Vec2 i[];
  polygonMesh_recomputeTangents_ComputeBiNormTask<<<1@true>>>(a, b, c, d, e, f, g, h, i);
}
inline __compile_polygonMesh_recomputeTangents_computeVertexTanTask(){
  Vec4 a[];  Vec3 b[];  Vec3 c[];  Vec3 d[];
  polygonMesh_recomputeTangents_computeVertexTanTask<<<1@true>>>(a, b, c, d);
}
inline __compile_polygonMesh_recomputeTangents_countPolygonsTask(){
  PolygonMeshTopology a;  Size b; Size c; UInt32 d[]; UInt32 e[];
  polygonMesh_recomputeTangents_countPolygonsTask<<<1@true>>>(a, b, c, d, e);
}

inline __compile_deltaMushModifier_smoothPos() { PolygonMeshTopology a; Vec3 b[]; deltaMushModifier_smoothPos<<<1@true>>>(a, b); }
inline __compile_deltaMushModifier_computePointBinding() { PolygonMeshTopology a; Vec3 b[];Vec3 c[];Vec3 d[]; deltaMushModifier_computePointBinding<<<1@true>>>(a, b, c, d); }
inline __compile_deltaMushModifier_applyDeltas() { PolygonMeshTopology a; Vec3 b[];Vec3 c[];Vec3 d[]; Boolean e; DebugLines f; deltaMushModifier_applyDeltas<<<1@true>>>(a, b, c, d, e, f); }
inline __compile_deltaMushModifier_applyDeltas_Masked() { PolygonMeshTopology a; Vec3 b[];Vec3 c[];Vec3 d[]; Scalar e[]; Boolean f; DebugLines g; deltaMushModifier_applyDeltas_Masked<<<1@true>>>(a, b, c, d, e, f, g); }

inline __compile_wrapModifier_applyDeltas(){
  PolygonMeshTopology a; Vec3 b[]; Vec3 c[]; Vec4 d[]; GeometryLocation e[]; Vec3 f[]; Vec3 g[]; Vec3 h[]; Vec3 i[]; Boolean j; DebugLines k;
  wrapModifier_applyDeltas<<<1@true>>>(a,b,c,d,e,f,g,h,i,j,k);
}

operator tubeCharacter_Skinning(
  io GeometryStack stack,
  Mat44 deformers[],
  Boolean displayDebugging
) {
  if(stack.numGeometryOperators() >= 2){
    SkinningModifier skinningModifier = stack.getGeometryOperator(1);
    skinningModifier.setPose(deformers);
    skinningModifier.setDisplayDebugging(displayDebugging);
  }
}
""")

cmds.connectAttr(influenceInitNode + '.stack', influencePoseNode + '.stack')


##############################################
## Set up the eval/render node.

influenceEvalNode = cmds.createNode("spliceMayaNode", name = "tubeCharacter_Eval")

cmds.fabricSplice('addInputPort', influenceEvalNode, json.dumps({'portName':'stack', 'dataType':'GeometryStack', 'extension':'RiggingToolbox', 'addSpliceMayaAttr':True, 'autoInitObjects': False}))
cmds.fabricSplice('addOutputPort', influenceEvalNode, json.dumps({'portName':'eval', 'dataType':'Scalar', 'addMayaAttr': True}))


cmds.fabricSplice('addInputPort', influenceEvalNode, json.dumps({'portName':'displayGeometries', 'dataType':'Boolean', 'addMayaAttr': True}))
cmds.setAttr(influenceEvalNode + '.displayGeometries', 1);

cmds.connectAttr(influencePoseNode + '.stack', influenceEvalNode + '.stack')

cmds.fabricSplice('addKLOperator', influenceEvalNode, '{"opName":"tubeCharacter_Eval"}', """

require RiggingToolbox;


inline __compile_Vec3Attribute_copyFrom() { Vec3 a[]; Vec3 b[]; Vec3Attribute_copyFrom<<<1@true>>>(a, b); }

// Skinning GPU Kernels
inline __compile_SkinningAttribute_copyFrom() { SkinningAttributeData a; SkinningAttributeData b; SkinningAttribute_copyFrom<<<1@true>>>(a, b); }
inline __compile_skinningModifier_skinMeshPositions() { 
  PolygonMeshTopology a; Vec3 b[]; SkinningAttributeData d; Mat44 e[]; skinningModifier_skinMeshPositions<<<1@true>>>(a,b, d, e); 
}
inline __compile_skinningModifier_skinMeshPositionsAndNormals() { 
  PolygonMeshTopology a; Vec3 b[]; Vec3 c[]; SkinningAttributeData d; Mat44 e[]; skinningModifier_skinMeshPositionsAndNormals<<<1@true>>>(a, b, c, d, e); 
}

// Compute Normals GPU Kernels
inline __compile_computeNormalsModifier_computePointNormals() { 
  PolygonMeshTopology a; Vec3 b[];Vec3 c[];Boolean d; DebugLines e; computeNormalsModifier_computePointNormals<<<1@true>>>(a, b, c, d, e); 
}

// Compute Tangents GPU Kernels
inline __compile_polygonMesh_recomputeTangents_setTangentTask() { 
  PolygonMeshTopology a; Vec4 b[];Vec4 c[]; 
  polygonMesh_recomputeTangents_setTangentTask<<<1@true>>>(a, b, c); 
}

inline __compile_polygonMesh_recomputeTangents_ComputeBiNormTask(){
  UInt32 a[];  UInt32 b[];  Vec3 c[];  Vec3 d[];  Vec3 e[];  Vec3 f[];  PolygonMeshTopology g;  Vec3 h[];  Vec2 i[];
  polygonMesh_recomputeTangents_ComputeBiNormTask<<<1@true>>>(a, b, c, d, e, f, g, h, i);
}
inline __compile_polygonMesh_recomputeTangents_computeVertexTanTask(){
  Vec4 a[];  Vec3 b[];  Vec3 c[];  Vec3 d[];
  polygonMesh_recomputeTangents_computeVertexTanTask<<<1@true>>>(a, b, c, d);
}
inline __compile_polygonMesh_recomputeTangents_countPolygonsTask(){
  PolygonMeshTopology a;  Size b; Size c; UInt32 d[]; UInt32 e[];
  polygonMesh_recomputeTangents_countPolygonsTask<<<1@true>>>(a, b, c, d, e);
}

inline __compile_deltaMushModifier_smoothPos() { PolygonMeshTopology a; Vec3 b[]; deltaMushModifier_smoothPos<<<1@true>>>(a, b); }
inline __compile_deltaMushModifier_computePointBinding() { PolygonMeshTopology a; Vec3 b[];Vec3 c[];Vec3 d[]; deltaMushModifier_computePointBinding<<<1@true>>>(a, b, c, d); }
inline __compile_deltaMushModifier_applyDeltas() { PolygonMeshTopology a; Vec3 b[];Vec3 c[];Vec3 d[]; Boolean e; DebugLines f; deltaMushModifier_applyDeltas<<<1@true>>>(a, b, c, d, e, f); }
inline __compile_deltaMushModifier_applyDeltas_Masked() { PolygonMeshTopology a; Vec3 b[];Vec3 c[];Vec3 d[]; Scalar e[]; Boolean f; DebugLines g; deltaMushModifier_applyDeltas_Masked<<<1@true>>>(a, b, c, d, e, f, g); }

inline __compile_wrapModifier_applyDeltas(){
  PolygonMeshTopology a; Vec3 b[]; Vec3 c[]; Vec4 d[]; GeometryLocation e[]; Vec3 f[]; Vec3 g[]; Vec3 h[]; Vec3 i[]; Boolean j; DebugLines k;
  wrapModifier_applyDeltas<<<1@true>>>(a,b,c,d,e,f,g,h,i,j,k);
}

operator tubeCharacter_Eval(
  io GeometryStack stack,
  Boolean displayGeometries,
  EvalContext context,
  Scalar eval
) {
  stack.setDisplayGeometries(displayGeometries);
  stack.evaluate(context);
}
""")



##############################################
## Set up the loader node for the wraped geoms

wrappedGeomsInitNode = cmds.createNode("spliceMayaNode", name = "wrappedGeoms_Init")

cmds.fabricSplice('addInputPort', wrappedGeomsInitNode, json.dumps({'portName':'filePath', 'dataType':'String', 'addMayaAttr': True}))
cmds.fabricSplice('addOutputPort', wrappedGeomsInitNode, json.dumps({'portName':'stack', 'dataType':'GeometryStack', 'extension':'RiggingToolbox', 'addSpliceMayaAttr':True, 'autoInitObjects': True}))

cmds.setAttr(wrappedGeomsInitNode + '.filePath', toolboxPath+"/Tests/GeometryStack/Resources/tubeCharacter_Wrap.json", type="string");


cmds.fabricSplice('addKLOperator', wrappedGeomsInitNode, '{"opName":"wrappedGeoms_Init"}', """

require RiggingToolbox;


inline __compile_Vec3Attribute_copyFrom() { Vec3 a[]; Vec3 b[]; Vec3Attribute_copyFrom<<<1@true>>>(a, b); }

// Skinning GPU Kernels
inline __compile_SkinningAttribute_copyFrom() { SkinningAttributeData a; SkinningAttributeData b; SkinningAttribute_copyFrom<<<1@true>>>(a, b); }
inline __compile_skinningModifier_skinMeshPositions() { 
  PolygonMeshTopology a; Vec3 b[]; SkinningAttributeData d; Mat44 e[]; skinningModifier_skinMeshPositions<<<1@true>>>(a,b, d, e); 
}
inline __compile_skinningModifier_skinMeshPositionsAndNormals() { 
  PolygonMeshTopology a; Vec3 b[]; Vec3 c[]; SkinningAttributeData d; Mat44 e[]; skinningModifier_skinMeshPositionsAndNormals<<<1@true>>>(a, b, c, d, e); 
}

// Compute Normals GPU Kernels
inline __compile_computeNormalsModifier_computePointNormals() { 
  PolygonMeshTopology a; Vec3 b[];Vec3 c[];Boolean d; DebugLines e; computeNormalsModifier_computePointNormals<<<1@true>>>(a, b, c, d, e); 
}

// Compute Tangents GPU Kernels
inline __compile_polygonMesh_recomputeTangents_setTangentTask() { 
  PolygonMeshTopology a; Vec4 b[];Vec4 c[]; 
  polygonMesh_recomputeTangents_setTangentTask<<<1@true>>>(a, b, c); 
}

inline __compile_polygonMesh_recomputeTangents_ComputeBiNormTask(){
  UInt32 a[];  UInt32 b[];  Vec3 c[];  Vec3 d[];  Vec3 e[];  Vec3 f[];  PolygonMeshTopology g;  Vec3 h[];  Vec2 i[];
  polygonMesh_recomputeTangents_ComputeBiNormTask<<<1@true>>>(a, b, c, d, e, f, g, h, i);
}
inline __compile_polygonMesh_recomputeTangents_computeVertexTanTask(){
  Vec4 a[];  Vec3 b[];  Vec3 c[];  Vec3 d[];
  polygonMesh_recomputeTangents_computeVertexTanTask<<<1@true>>>(a, b, c, d);
}
inline __compile_polygonMesh_recomputeTangents_countPolygonsTask(){
  PolygonMeshTopology a;  Size b; Size c; UInt32 d[]; UInt32 e[];
  polygonMesh_recomputeTangents_countPolygonsTask<<<1@true>>>(a, b, c, d, e);
}

inline __compile_deltaMushModifier_smoothPos() { PolygonMeshTopology a; Vec3 b[]; deltaMushModifier_smoothPos<<<1@true>>>(a, b); }
inline __compile_deltaMushModifier_computePointBinding() { PolygonMeshTopology a; Vec3 b[];Vec3 c[];Vec3 d[]; deltaMushModifier_computePointBinding<<<1@true>>>(a, b, c, d); }
inline __compile_deltaMushModifier_applyDeltas() { PolygonMeshTopology a; Vec3 b[];Vec3 c[];Vec3 d[]; Boolean e; DebugLines f; deltaMushModifier_applyDeltas<<<1@true>>>(a, b, c, d, e, f); }
inline __compile_deltaMushModifier_applyDeltas_Masked() { PolygonMeshTopology a; Vec3 b[];Vec3 c[];Vec3 d[]; Scalar e[]; Boolean f; DebugLines g; deltaMushModifier_applyDeltas_Masked<<<1@true>>>(a, b, c, d, e, f, g); }

inline __compile_wrapModifier_applyDeltas(){
  PolygonMeshTopology a; Vec3 b[]; Vec3 c[]; Vec4 d[]; GeometryLocation e[]; Vec3 f[]; Vec3 g[]; Vec3 h[]; Vec3 i[]; Boolean j; DebugLines k;
  wrapModifier_applyDeltas<<<1@true>>>(a,b,c,d,e,f,g,h,i,j,k);
}

operator wrappedGeoms_Init(
  String filePath,
  io GeometryStack stack
) {
  //StartFabricProfiling();

  report("Loading Character Definition:" + filePath);
  stack.loadJSONFile(filePath);
}
""")
  
##############################################
## Set up the eval/render node.

wrappedGeomsEvalNode = cmds.createNode("spliceMayaNode", name = "wrappedGeoms_Eval")

cmds.fabricSplice('addInputPort', wrappedGeomsEvalNode, json.dumps({'portName':'stack', 'dataType':'GeometryStack', 'extension':'RiggingToolbox', 'addSpliceMayaAttr':True, 'autoInitObjects': False}))
cmds.fabricSplice('addInputPort', wrappedGeomsEvalNode, json.dumps({'portName':'srcstack', 'dataType':'GeometryStack', 'extension':'RiggingToolbox', 'addSpliceMayaAttr':True, 'autoInitObjects': False}))
cmds.fabricSplice('addOutputPort', wrappedGeomsEvalNode, json.dumps({'portName':'eval', 'dataType':'Scalar', 'addMayaAttr': True}))
cmds.fabricSplice('addInputPort', wrappedGeomsEvalNode, json.dumps({'portName':'displayDebugging', 'dataType':'Boolean', 'addMayaAttr': True}))

cmds.connectAttr(wrappedGeomsInitNode + '.stack', wrappedGeomsEvalNode + '.stack')
cmds.connectAttr(influenceEvalNode + '.stack', wrappedGeomsEvalNode + '.srcstack')

cmds.fabricSplice('addKLOperator', wrappedGeomsEvalNode, '{"opName":"wrappedGeoms_Eval"}', """

require RiggingToolbox;


inline __compile_Vec3Attribute_copyFrom() { Vec3 a[]; Vec3 b[]; Vec3Attribute_copyFrom<<<1@true>>>(a, b); }

// Skinning GPU Kernels
inline __compile_SkinningAttribute_copyFrom() { SkinningAttributeData a; SkinningAttributeData b; SkinningAttribute_copyFrom<<<1@true>>>(a, b); }
inline __compile_skinningModifier_skinMeshPositions() { 
  PolygonMeshTopology a; Vec3 b[]; SkinningAttributeData d; Mat44 e[]; skinningModifier_skinMeshPositions<<<1@true>>>(a,b, d, e); 
}
inline __compile_skinningModifier_skinMeshPositionsAndNormals() { 
  PolygonMeshTopology a; Vec3 b[]; Vec3 c[]; SkinningAttributeData d; Mat44 e[]; skinningModifier_skinMeshPositionsAndNormals<<<1@true>>>(a, b, c, d, e); 
}

// Compute Normals GPU Kernels
inline __compile_computeNormalsModifier_computePointNormals() { 
  PolygonMeshTopology a; Vec3 b[];Vec3 c[];Boolean d; DebugLines e; computeNormalsModifier_computePointNormals<<<1@true>>>(a, b, c, d, e); 
}

// Compute Tangents GPU Kernels
inline __compile_polygonMesh_recomputeTangents_setTangentTask() { 
  PolygonMeshTopology a; Vec4 b[];Vec4 c[]; 
  polygonMesh_recomputeTangents_setTangentTask<<<1@true>>>(a, b, c); 
}

inline __compile_polygonMesh_recomputeTangents_ComputeBiNormTask(){
  UInt32 a[];  UInt32 b[];  Vec3 c[];  Vec3 d[];  Vec3 e[];  Vec3 f[];  PolygonMeshTopology g;  Vec3 h[];  Vec2 i[];
  polygonMesh_recomputeTangents_ComputeBiNormTask<<<1@true>>>(a, b, c, d, e, f, g, h, i);
}
inline __compile_polygonMesh_recomputeTangents_computeVertexTanTask(){
  Vec4 a[];  Vec3 b[];  Vec3 c[];  Vec3 d[];
  polygonMesh_recomputeTangents_computeVertexTanTask<<<1@true>>>(a, b, c, d);
}
inline __compile_polygonMesh_recomputeTangents_countPolygonsTask(){
  PolygonMeshTopology a;  Size b; Size c; UInt32 d[]; UInt32 e[];
  polygonMesh_recomputeTangents_countPolygonsTask<<<1@true>>>(a, b, c, d, e);
}

inline __compile_deltaMushModifier_smoothPos() { PolygonMeshTopology a; Vec3 b[]; deltaMushModifier_smoothPos<<<1@true>>>(a, b); }
inline __compile_deltaMushModifier_computePointBinding() { PolygonMeshTopology a; Vec3 b[];Vec3 c[];Vec3 d[]; deltaMushModifier_computePointBinding<<<1@true>>>(a, b, c, d); }
inline __compile_deltaMushModifier_applyDeltas() { PolygonMeshTopology a; Vec3 b[];Vec3 c[];Vec3 d[]; Boolean e; DebugLines f; deltaMushModifier_applyDeltas<<<1@true>>>(a, b, c, d, e, f); }
inline __compile_deltaMushModifier_applyDeltas_Masked() { PolygonMeshTopology a; Vec3 b[];Vec3 c[];Vec3 d[]; Scalar e[]; Boolean f; DebugLines g; deltaMushModifier_applyDeltas_Masked<<<1@true>>>(a, b, c, d, e, f, g); }

inline __compile_wrapModifier_applyDeltas(){
  PolygonMeshTopology a; Vec3 b[]; Vec3 c[]; Vec4 d[]; GeometryLocation e[]; Vec3 f[]; Vec3 g[]; Vec3 h[]; Vec3 i[]; Boolean j; DebugLines k;
  wrapModifier_applyDeltas<<<1@true>>>(a,b,c,d,e,f,g,h,i,j,k);
}

operator wrappedGeoms_Eval(
  io GeometryStack stack,
  io GeometryStack srcstack,
  Boolean displayDebugging,
  Scalar eval
) {
  if(stack.numGeometryOperators() >= 2){
    WrapModifier wrapModifier = stack.getGeometryOperator(1);
    wrapModifier.setSourceGeomStack(srcstack);
    wrapModifier.setDisplayDebugging(displayDebugging);
  }

  //StartFabricProfiling();

  EvalContext context();
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
cmds.connectAttr(wrappedGeomsEvalNode + '.eval', forceEvalLocator + '.localPosition.localPositionY')
