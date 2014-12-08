
import json
from maya import cmds

# cmds.file(new=True,f=True)
# cmds.file("D:/Resources/captainatom_project/scenes/captainatom_v1_geomStripped.mb", r=True);


##############################################
## Set up the loader node.

influenceInitNode = cmds.createNode("spliceMayaNode", name = "captainAtom_Init")

cmds.fabricSplice('addInputPort', influenceInitNode, json.dumps({'portName':'filePath', 'dataType':'String', 'addMayaAttr': True}))
cmds.fabricSplice('addOutputPort', influenceInitNode, json.dumps({'portName':'stack', 'dataType':'GeometryStack', 'extension':'RiggingToolbox', 'addSpliceMayaAttr':True, 'autoInitObjects': True}))

cmds.setAttr(influenceInitNode + '.filePath', "D:/Projects/RiggingToolbox/Tests/GeometryStack/Resources/CaptainAtom_Skinning.json", type="string");


cmds.fabricSplice('addKLOperator', influenceInitNode, '{"opName":"captainAtom_Init"}', """

require RiggingToolbox;

operator captainAtom_Init(
  String filePath,
  io GeometryStack stack
) {

  report("Loading Character Definition:" + filePath);
  stack.loadJSONFile(filePath);
}
""")
  

##############################################
## Set up the skinning pose node.

influencePoseNode = cmds.createNode("spliceMayaNode", name = "captainAtom_SetPose")

cmds.fabricSplice('addIOPort', influencePoseNode, json.dumps({'portName':'stack', 'dataType':'GeometryStack', 'extension':'RiggingToolbox', 'addSpliceMayaAttr':True, 'autoInitObjects': False }))
cmds.fabricSplice('addInputPort', influencePoseNode, json.dumps({'portName':'displayDebugging', 'dataType':'Boolean', 'addMayaAttr': True}))
cmds.fabricSplice('addInputPort', influencePoseNode, json.dumps({'portName':'deformers', 'dataType':'Mat44[]', 'addMayaAttr': True, 'arrayType':"Array (Multi)"}))

deformers = [ "captainatom_hip_joint", "captainatom_spine_ik_2_joint", "captainatom_spine_ik_3_joint", "captainatom_spine_ik_4_joint", "captainatom_spine_ik_5_joint", "captainatom_spine_ik_6_joint", "captainatom_chest_joint", "captainatom_L_main_thigh_joint", "captainatom_L_main_knee_joint", "captainatom_L_main_ankle_joint", "captainatom_L_main_ball_joint", "captainatom_R_main_thigh_joint", "captainatom_R_main_knee_joint", "captainatom_R_main_ankle_joint", "captainatom_R_main_ball_joint", "captainatom_L_thigh_bendy_joint", "captainatom_L_knee_bendy_joint", "captainatom_L_thighBase_joint", "captainatom_L_kneeBase_joint", "captainatom_R_thigh_bendy_joint", "captainatom_R_knee_bendy_joint", "captainatom_R_thighBase_joint", "captainatom_R_kneeBase_joint", "captainatom_neck_joint", "captainatom_head_joint", "captainatom_L_clavicle_joint", "captainatom_R_clavicle_joint", "captainatom_L_main_shoulder_joint", "captainatom_L_main_elbow_joint", "captainatom_L_main_wrist_joint", "captainatom_L_finger_mid_base_joint", "captainatom_L_finger_mid_1_joint", "captainatom_L_finger_mid_2_joint", "captainatom_L_finger_mid_3_joint", "captainatom_L_finger_pointer_base_joint", "captainatom_L_finger_pointer_1_joint", "captainatom_L_finger_pointer_2_joint", "captainatom_L_finger_pointer_3_joint", "captainatom_L_finger_ring_base_joint", "captainatom_L_finger_ring_1_joint", "captainatom_L_finger_ring_2_joint", "captainatom_L_finger_ring_3_joint", "captainatom_L_finger_pinky_base_joint", "captainatom_L_finger_pinky_cup_joint", "captainatom_L_finger_pinky_1_joint", "captainatom_L_finger_pinky_2_joint", "captainatom_L_finger_pinky_3_joint", "captainatom_L_finger_thumb_base_joint", "captainatom_L_finger_thumb_1_joint", "captainatom_L_finger_thumb_2_joint", "captainatom_R_main_shoulder_joint", "captainatom_R_main_elbow_joint", "captainatom_R_main_wrist_joint", "captainatom_R_finger_mid_base_joint", "captainatom_R_finger_mid_1_joint", "captainatom_R_finger_mid_2_joint", "captainatom_R_finger_mid_3_joint", "captainatom_R_finger_pointer_base_joint", "captainatom_R_finger_pointer_1_joint", "captainatom_R_finger_pointer_2_joint", "captainatom_R_finger_pointer_3_joint", "captainatom_R_finger_ring_base_joint", "captainatom_R_finger_ring_1_joint", "captainatom_R_finger_ring_2_joint", "captainatom_R_finger_ring_3_joint", "captainatom_R_finger_pinky_base_joint", "captainatom_R_finger_pinky_cup_joint", "captainatom_R_finger_pinky_1_joint", "captainatom_R_finger_pinky_2_joint", "captainatom_R_finger_pinky_3_joint", "captainatom_R_finger_thumb_base_joint", "captainatom_R_finger_thumb_1_joint", "captainatom_R_finger_thumb_2_joint", "captainatom_L_shoulder_bendy_joint", "captainatom_L_shoulderBase_joint", "captainatom_R_shoulder_bendy_joint", "captainatom_R_shoulderBase_joint", "captainatom_L_forearm_1_joint", "captainatom_L_forearm_2_joint", "captainatom_R_forearm_1_joint", "captainatom_R_forearm_2_joint", "captainatom_onFace_upperLip_joint", "captainatom_onFace_lowerLip_joint", "captainatom_L_onFace_upperLip_joint", "captainatom_L_onFace_lowerLip_joint", "captainatom_L_onFace_lip_joint", "captainatom_R_onFace_upperLip_joint", "captainatom_R_onFace_lowerLip_joint", "captainatom_R_onFace_lip_joint", "captainatom_L_onFace_nose_joint", "captainatom_R_onFace_nose_joint", "captainatom_L_onFace_cheek2_joint", "captainatom_R_onFace_cheek2_joint", "captainatom_L_onFace_eyeBrow1_joint", "captainatom_L_onFace_eyeBrow2_joint", "captainatom_L_onFace_eyeBrow3_joint", "captainatom_R_onFace_eyeBrow1_joint", "captainatom_R_onFace_eyeBrow2_joint", "captainatom_R_onFace_eyeBrow3_joint", "captainatom_jaw_joint", "captainatom_L_onFace_cheek1_joint", "captainatom_R_onFace_cheek1_joint", "captainatom_L_onFace_upperLid_joint", "captainatom_L_onFace_lowerLid_joint", "captainatom_R_onFace_upperLid_joint", "captainatom_R_onFace_lowerLid_joint"]
deformerPorts = ""
deformerKLArray = ""
for i in range(len(deformers)):
  cmds.connectAttr(deformers[i]+'.worldMatrix[0]', influencePoseNode + '.deformers[' + str(i) + ']')

cmds.fabricSplice('addKLOperator', influencePoseNode, '{"opName":"captainAtom_SetPose"}', """

require RiggingToolbox;

operator captainAtom_SetPose(
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
## Set up the delta mush node.

influenceMushNode = cmds.createNode("spliceMayaNode", name = "captainAtom_DeltaMush")

cmds.fabricSplice('addIOPort', influenceMushNode, json.dumps({'portName':'stack', 'dataType':'GeometryStack', 'extension':'RiggingToolbox', 'addSpliceMayaAttr':True, 'autoInitObjects': False }))
cmds.fabricSplice('addInputPort', influenceMushNode, json.dumps({'portName':'iterations', 'dataType':'Integer', 'addMayaAttr': True}))
cmds.fabricSplice('addInputPort', influenceMushNode, json.dumps({'portName':'displayDebugging', 'dataType':'Boolean', 'addMayaAttr': True}))

cmds.setAttr(influenceMushNode + '.iterations', 30);

cmds.fabricSplice('addKLOperator', influenceMushNode, '{"opName":"captainAtom_DeltaMush"}', """

require RiggingToolbox;

operator captainAtom_DeltaMush(
  io GeometryStack stack,
  Integer iterations,
  Boolean displayDebugging
) {
  if(stack.numGeometryOperators() >= 3){
    DeltaMushModifier deltaMushModifier = stack.getGeometryOperator(2);
    deltaMushModifier.setNumIterations(iterations);
    deltaMushModifier.setDisplayDebugging(displayDebugging);
  }
}
""")

cmds.connectAttr(influencePoseNode + '.stack', influenceMushNode + '.stack')


##############################################
## Set up the eval/render node.

influenceEvalNode = cmds.createNode("spliceMayaNode", name = "captainAtom_EvalSkinning")

cmds.fabricSplice('addInputPort', influenceEvalNode, json.dumps({'portName':'stack', 'dataType':'GeometryStack', 'extension':'RiggingToolbox', 'addSpliceMayaAttr':True, 'autoInitObjects': False}))
cmds.fabricSplice('addOutputPort', influenceEvalNode, json.dumps({'portName':'eval', 'dataType':'Scalar', 'addMayaAttr': True}))
cmds.fabricSplice('addInputPort', influenceEvalNode, json.dumps({'portName':'displayGeometries', 'dataType':'Boolean', 'addMayaAttr': True}))

cmds.connectAttr(influenceMushNode + '.stack', influenceEvalNode + '.stack')

cmds.fabricSplice('addKLOperator', influenceEvalNode, '{"opName":"captainAtom_EvalSkinning"}', """

require RiggingToolbox;

operator captainAtom_EvalSkinning(
  io GeometryStack stack,
  Boolean displayGeometries,
  Scalar eval
) {
  if(displayGeometries){
    stack.setDisplayGeometries(displayGeometries);
    EvalContext context();
    stack.evaluate(context);
  }
}
""")


##############################################
## Set up the loader node for the wraped geoms

wrappedGeomsInitNode = cmds.createNode("spliceMayaNode", name = "wrappedGeoms_Init")

cmds.fabricSplice('addInputPort', wrappedGeomsInitNode, json.dumps({'portName':'filePath', 'dataType':'String', 'addMayaAttr': True}))
cmds.fabricSplice('addOutputPort', wrappedGeomsInitNode, json.dumps({'portName':'stack', 'dataType':'GeometryStack', 'extension':'RiggingToolbox', 'addSpliceMayaAttr':True, 'autoInitObjects': True}))

cmds.setAttr(wrappedGeomsInitNode + '.filePath', "D:/Projects/RiggingToolbox/Tests/GeometryStack/Resources/CaptainAtom_Wrapped.json", type="string");


cmds.fabricSplice('addKLOperator', wrappedGeomsInitNode, '{"opName":"wrappedGeoms_Init"}', """

require RiggingToolbox;

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
cmds.fabricSplice('addInputPort', wrappedGeomsEvalNode, json.dumps({'portName':'displayGeometries', 'dataType':'Boolean', 'addMayaAttr': True}))
cmds.fabricSplice('addOutputPort', wrappedGeomsEvalNode, json.dumps({'portName':'eval', 'dataType':'Scalar', 'addMayaAttr': True}))
cmds.setAttr(wrappedGeomsEvalNode + '.displayGeometries', 1);


cmds.connectAttr(wrappedGeomsInitNode + '.stack', wrappedGeomsEvalNode + '.stack')
cmds.connectAttr(influenceEvalNode + '.stack', wrappedGeomsEvalNode + '.srcstack')

cmds.fabricSplice('addKLOperator', wrappedGeomsEvalNode, '{"opName":"wrappedGeoms_Eval"}', """

require RiggingToolbox;

operator wrappedGeoms_Eval(
  io GeometryStack stack,
  io GeometryStack srcstack,
  Boolean displayGeometries,
  Scalar eval
) {
  if(stack.numGeometryOperators() >= 2){
    WrapModifier wrapModifier = stack.getGeometryOperator(1);
    wrapModifier.setSourceGeomStack(srcstack);
  }
  stack.setDisplayGeometries(displayGeometries);

  UInt64 start = getCurrentTicks();

  //StartFabricProfiling();

  EvalContext context();
  stack.evaluate(context);

  //StopFabricProfiling();
  //report( GetProfilingReport() );

  UInt64 end = getCurrentTicks();
  report("Eval Fps: " + String(1.0 / getSecondsBetweenTicks(start, end)));


  //report(stack.getDesc());
}
""")

##############################################
## Set up the eval locator.

forceEvalLocator = cmds.createNode("locator", name = "forceEval")
cmds.connectAttr(wrappedGeomsEvalNode + '.eval', forceEvalLocator + '.localPosition.localPositionY')
