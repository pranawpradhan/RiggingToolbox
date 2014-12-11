
import json
from maya import cmds

# cmds.file(new=True,f=True)
# cmds.file("D:/Resources/captainatom_project/scenes/captainatom_v1_geomStripped.mb", r=True);


##############################################
## Set up the loader node.

influenceGeoms_Node = cmds.createNode("spliceMayaNode", name = "captainAtom_InfluenceGeoms")

cmds.fabricSplice('addInputPort', influenceGeoms_Node, json.dumps({'portName':'filePath', 'dataType':'String', 'addMayaAttr': True}))
cmds.fabricSplice('addOutputPort', influenceGeoms_Node, json.dumps({'portName':'stack', 'dataType':'GeometryStack', 'extension':'RiggingToolbox', 'addSpliceMayaAttr':True, 'autoInitObjects': True}))
cmds.fabricSplice('addInputPort', influenceGeoms_Node, json.dumps({'portName':'displaySkinningDebugging', 'dataType':'Boolean', 'addMayaAttr': True}))
cmds.fabricSplice('addInputPort', influenceGeoms_Node, json.dumps({'portName':'iterations', 'dataType':'Integer', 'addMayaAttr': True}))
cmds.fabricSplice('addInputPort', influenceGeoms_Node, json.dumps({'portName':'useDeltaMushMask', 'dataType':'Boolean', 'addMayaAttr': True}))
cmds.fabricSplice('addInputPort', influenceGeoms_Node, json.dumps({'portName':'displayDeltaMushMask', 'dataType':'Boolean', 'addMayaAttr': True}))
cmds.fabricSplice('addInputPort', influenceGeoms_Node, json.dumps({'portName':'displayDeltaMushDebugging', 'dataType':'Boolean', 'addMayaAttr': True}))
cmds.fabricSplice('addInputPort', influenceGeoms_Node, json.dumps({'portName':'displayGeometries', 'dataType':'Boolean', 'addMayaAttr': True}))
cmds.fabricSplice('addInputPort', influenceGeoms_Node, json.dumps({'portName':'deformers', 'dataType':'Mat44[]', 'addMayaAttr': True, 'arrayType':"Array (Multi)"}))


cmds.fabricSplice('addKLOperator', influenceGeoms_Node, '{"opName":"captainAtom_InfluenceGeoms"}', """

require RiggingToolbox;

operator captainAtom_InfluenceGeoms(
  String filePath,
  io GeometryStack stack,
  Boolean displaySkinningDebugging,
  Integer iterations,
  Boolean useDeltaMushMask,
  Boolean displayDeltaMushMask,
  Boolean displayDeltaMushDebugging,
  Boolean displayGeometries,
  Mat44 deformers[],
  EvalContext context
) {
  report("captainAtom_InfluenceGeoms:" + context._dirtyInputs);
  if(context.isInputDirty('filePath')){
    report("Loading Character Definition:" + filePath);
    stack.loadJSONFile(filePath);
  }

  if(context.isInputDirty('deformers') || context.isInputDirty('displaySkinningDebugging')){
    if(stack.numGeometryOperators() > 1){
      SkinningModifier skinningModifier = stack.getGeometryOperator(1);
      skinningModifier.setPose(deformers);
      skinningModifier.setDisplayDebugging(displaySkinningDebugging);
    }
  }
  if(context.isInputDirty('iterations') || context.isInputDirty('displayDeltaMushMask') || context.isInputDirty('useDeltaMushMask') || context.isInputDirty('displayDeltaMushDebugging')){
    if(stack.numGeometryOperators() > 3){
      WeightmapModifier weightmapModifier = stack.getGeometryOperator(2);
      weightmapModifier.setDisplay(displayDeltaMushMask);

      DeltaMushModifier deltaMushModifier = stack.getGeometryOperator(3);
      deltaMushModifier.setNumIterations(iterations);
      deltaMushModifier.setUseMask(useDeltaMushMask);
      deltaMushModifier.setDisplayDebugging(displayDeltaMushMask);
      deltaMushModifier.setDisplayDebugging(displayDeltaMushDebugging);
    }
  }
  if(context.isInputDirty('displayGeometries')){
    stack.setDisplayGeometries(displayGeometries);
    if(displayGeometries){
      stack.evaluate(context);
    }
  }
}
""")



##############################################
## Set up the loader node for the render geoms

renderGeoms_Node = cmds.createNode("spliceMayaNode", name = "captainAtom_RenderGeoms")

cmds.fabricSplice('addInputPort', renderGeoms_Node, json.dumps({'portName':'filePath', 'dataType':'String', 'addMayaAttr': True}))
cmds.fabricSplice('addOutputPort', renderGeoms_Node, json.dumps({'portName':'stack', 'dataType':'GeometryStack', 'extension':'RiggingToolbox', 'addSpliceMayaAttr':True, 'autoInitObjects': True}))
cmds.fabricSplice('addInputPort', renderGeoms_Node, json.dumps({'portName':'srcstack', 'dataType':'GeometryStack', 'extension':'RiggingToolbox', 'addSpliceMayaAttr':True, 'autoInitObjects': False}))
cmds.fabricSplice('addInputPort', renderGeoms_Node, json.dumps({'portName':'displayDebugging', 'dataType':'Boolean', 'addMayaAttr': True}))
cmds.fabricSplice('addInputPort', renderGeoms_Node, json.dumps({'portName':'displayGeometries', 'dataType':'Boolean', 'addMayaAttr': True}))
cmds.fabricSplice('addOutputPort', renderGeoms_Node, json.dumps({'portName':'eval', 'dataType':'Scalar', 'addMayaAttr': True}))
cmds.setAttr(renderGeoms_Node + '.displayGeometries', 1);

cmds.fabricSplice('addKLOperator', renderGeoms_Node, '{"opName":"captainAtom_RenderGeoms"}', """

require RiggingToolbox;

operator captainAtom_RenderGeoms(
  String filePath,
  io GeometryStack stack,
  io GeometryStack srcstack,
  Boolean displayDebugging,
  Boolean displayGeometries,
  EvalContext context,
  Scalar eval
) {
  report("captainAtom_RenderGeoms:" + context._dirtyInputs);

  if(context.isInputDirty('filePath')){
    report("Loading Character Definition:" + filePath);
    stack.loadJSONFile(filePath);
  }

  if(context.isInputDirty('srcstack') || context.isInputDirty('displayDebugging')){
    if(stack.numGeometryOperators() > 1){
      WrapModifier wrapModifier = stack.getGeometryOperator(1);
      wrapModifier.setSourceGeomStack(srcstack);
      wrapModifier.setDisplayDebugging(displayDebugging);
    }
  }

  stack.setDisplayGeometries(displayGeometries);

  //UInt64 start = getCurrentTicks();
  //StartFabricProfiling();

  stack.evaluate(context);

  //StopFabricProfiling();
  //report( GetProfilingReport() );
  // UInt64 end = getCurrentTicks();
  // report("Eval Fps: " + String(1.0 / getSecondsBetweenTicks(start, end)));
  //report(stack.getDesc());
}
""")

##############################################
## Set up the eval locator.

forceEvalLocator = cmds.createNode("locator", name = "forceEval")

cmds.connectAttr(influenceGeoms_Node + '.stack', renderGeoms_Node + '.srcstack')
cmds.connectAttr(renderGeoms_Node + '.eval', forceEvalLocator + '.localPosition.localPositionY')

cmds.setAttr(influenceGeoms_Node + '.filePath', "D:/Projects/RiggingToolbox/Tests/GeometryStack/Resources/CaptainAtom_Skinning.json", type="string");
cmds.setAttr(renderGeoms_Node + '.filePath', "D:/Projects/RiggingToolbox/Tests/GeometryStack/Resources/CaptainAtom_Wrapped.json", type="string");

cmds.setAttr(influenceGeoms_Node + '.iterations', 30);
deformers   = ["captainatom_hip_joint","captainatom_spine_ik_2_joint","captainatom_spine_ik_3_joint","captainatom_spine_ik_4_joint","captainatom_spine_ik_5_joint","captainatom_spine_ik_6_joint","captainatom_chest_joint","captainatom_L_main_thigh_joint","captainatom_L_main_knee_joint","captainatom_L_main_ankle_joint","captainatom_L_main_ball_joint","captainatom_R_main_thigh_joint","captainatom_R_main_knee_joint","captainatom_R_main_ankle_joint","captainatom_R_main_ball_joint","captainatom_L_thigh_bendy_joint","captainatom_L_knee_bendy_joint","captainatom_L_thighBase_joint","captainatom_L_kneeBase_joint","captainatom_R_thigh_bendy_joint","captainatom_R_knee_bendy_joint","captainatom_R_thighBase_joint","captainatom_R_kneeBase_joint","captainatom_neck_joint","captainatom_head_joint","captainatom_L_clavicle_joint","captainatom_R_clavicle_joint","captainatom_L_main_shoulder_joint","captainatom_L_main_elbow_joint","captainatom_L_main_wrist_joint","captainatom_L_finger_mid_base_joint","captainatom_L_finger_mid_1_joint","captainatom_L_finger_mid_2_joint","captainatom_L_finger_mid_3_joint","captainatom_L_finger_pointer_base_joint","captainatom_L_finger_pointer_1_joint","captainatom_L_finger_pointer_2_joint","captainatom_L_finger_pointer_3_joint","captainatom_L_finger_ring_base_joint","captainatom_L_finger_ring_1_joint","captainatom_L_finger_ring_2_joint","captainatom_L_finger_ring_3_joint","captainatom_L_finger_pinky_base_joint","captainatom_L_finger_pinky_cup_joint","captainatom_L_finger_pinky_1_joint","captainatom_L_finger_pinky_2_joint","captainatom_L_finger_pinky_3_joint","captainatom_L_finger_thumb_base_joint","captainatom_L_finger_thumb_1_joint","captainatom_L_finger_thumb_2_joint","captainatom_R_main_shoulder_joint","captainatom_R_main_elbow_joint","captainatom_R_main_wrist_joint","captainatom_R_finger_mid_base_joint","captainatom_R_finger_mid_1_joint","captainatom_R_finger_mid_2_joint","captainatom_R_finger_mid_3_joint","captainatom_R_finger_pointer_base_joint","captainatom_R_finger_pointer_1_joint","captainatom_R_finger_pointer_2_joint","captainatom_R_finger_pointer_3_joint","captainatom_R_finger_ring_base_joint","captainatom_R_finger_ring_1_joint","captainatom_R_finger_ring_2_joint","captainatom_R_finger_ring_3_joint","captainatom_R_finger_pinky_base_joint","captainatom_R_finger_pinky_cup_joint","captainatom_R_finger_pinky_1_joint","captainatom_R_finger_pinky_2_joint","captainatom_R_finger_pinky_3_joint","captainatom_R_finger_thumb_base_joint","captainatom_R_finger_thumb_1_joint","captainatom_R_finger_thumb_2_joint","captainatom_L_shoulder_bendy_joint","captainatom_L_shoulderBase_joint","captainatom_R_shoulder_bendy_joint","captainatom_R_shoulderBase_joint","captainatom_L_forearm_1_joint","captainatom_L_forearm_2_joint","captainatom_R_forearm_1_joint","captainatom_R_forearm_2_joint","captainatom_onFace_upperLip_joint","captainatom_onFace_lowerLip_joint","captainatom_L_onFace_upperLip_joint","captainatom_L_onFace_lowerLip_joint","captainatom_L_onFace_lip_joint","captainatom_R_onFace_upperLip_joint","captainatom_R_onFace_lowerLip_joint","captainatom_R_onFace_lip_joint","captainatom_L_onFace_nose_joint","captainatom_R_onFace_nose_joint","captainatom_L_onFace_cheek2_joint","captainatom_R_onFace_cheek2_joint","captainatom_L_onFace_eyeBrow1_joint","captainatom_L_onFace_eyeBrow2_joint","captainatom_L_onFace_eyeBrow3_joint","captainatom_R_onFace_eyeBrow1_joint","captainatom_R_onFace_eyeBrow2_joint","captainatom_R_onFace_eyeBrow3_joint","captainatom_jaw_joint","captainatom_L_onFace_cheek1_joint","captainatom_R_onFace_cheek1_joint","captainatom_L_onFace_upperLid_joint","captainatom_L_onFace_lowerLid_joint","captainatom_R_onFace_upperLid_joint","captainatom_R_onFace_lowerLid_joint"]

for i in range(len(deformers)):
  cmds.connectAttr(deformers[i]+'.worldMatrix[0]', influenceGeoms_Node + '.deformers[' + str(i) + ']')