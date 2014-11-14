
import json
from maya import cmds

cmds.file(new=True,f=True)
cmds.file("C:/Users/Phil/Projects/RiggingToolbox/Tests/GeometryStack/Resources/SkinnedTube_hierarchy.ma", r=True);


##############################################
## Set up the loader node.

influenceInitNode = cmds.createNode("spliceMayaNode", name = "tubeCharacter_Init")

cmds.fabricSplice('addInputPort', influenceInitNode, json.dumps({'portName':'filePath', 'dataType':'String', 'addMayaAttr': True}))
cmds.fabricSplice('addOutputPort', influenceInitNode, json.dumps({'portName':'stack', 'dataType':'GeometryStack', 'extension':'RiggingToolbox', 'addSpliceMayaAttr':True, 'autoInitObjects': True}))

cmds.setAttr(influenceInitNode + '.filePath', "C:/Users/Phil/Projects/RiggingToolbox/Tests/GeometryStack/Resources/tubeCharacter_SkinningAndDeltaMush.json", type="string");


cmds.fabricSplice('addKLOperator', influenceInitNode, '{"opName":"tubeCharacter_Init"}', """

require RiggingToolbox;

operator tubeCharacter_Init(
  String filePath,
  io GeometryStack stack
) {
  //StartFabricProfiling();

  report("Loading Character Definition:" + filePath);
  stack.loadJSONFile(filePath);
}
""")
  

##############################################
## Set up the skinning pose node.

influencePoseNode = cmds.createNode("spliceMayaNode", name = "tubeCharacter_SetPose")

cmds.fabricSplice('addIOPort', influencePoseNode, json.dumps({'portName':'stack', 'dataType':'GeometryStack', 'extension':'RiggingToolbox', 'addSpliceMayaAttr':True, 'autoInitObjects': False }))
cmds.fabricSplice('addInputPort', influencePoseNode, json.dumps({'portName':'joint1', 'dataType':'Mat44', 'addMayaAttr': True}))
cmds.fabricSplice('addInputPort', influencePoseNode, json.dumps({'portName':'joint2', 'dataType':'Mat44', 'addMayaAttr': True}))
cmds.fabricSplice('addInputPort', influencePoseNode, json.dumps({'portName':'joint3', 'dataType':'Mat44', 'addMayaAttr': True}))
cmds.fabricSplice('addInputPort', influencePoseNode, json.dumps({'portName':'joint4', 'dataType':'Mat44', 'addMayaAttr': True}))

cmds.connectAttr('SkinnedTube_hierarchy_joint1.worldMatrix[0]', influencePoseNode + '.joint1')
cmds.connectAttr('SkinnedTube_hierarchy_joint2.worldMatrix[0]', influencePoseNode + '.joint2')
cmds.connectAttr('SkinnedTube_hierarchy_joint3.worldMatrix[0]', influencePoseNode + '.joint3')
cmds.connectAttr('SkinnedTube_hierarchy_joint4.worldMatrix[0]', influencePoseNode + '.joint4')

cmds.fabricSplice('addKLOperator', influencePoseNode, '{"opName":"tubeCharacter_SetPose"}', """

require RiggingToolbox;

operator tubeCharacter_SetPose(
  io GeometryStack stack,
  Mat44 joint1,
  Mat44 joint2,
  Mat44 joint3,
  Mat44 joint4
) {
  if(stack.numGeometryOperators() >= 2){
    SkinningModifier skinningModifier = stack.getGeometryOperator(1);
    Mat44 pose[];
    pose.push(joint1);
    pose.push(joint2);
    pose.push(joint3);
    pose.push(joint4);
    skinningModifier.setPose(pose);
  }
}
""")

cmds.connectAttr(influenceInitNode + '.stack', influencePoseNode + '.stack')


##############################################
## Set up the delta mush node.

influenceMushNode = cmds.createNode("spliceMayaNode", name = "tubeCharacter_DeltaMush")

cmds.fabricSplice('addIOPort', influenceMushNode, json.dumps({'portName':'stack', 'dataType':'GeometryStack', 'extension':'RiggingToolbox', 'addSpliceMayaAttr':True, 'autoInitObjects': False }))
cmds.fabricSplice('addInputPort', influenceMushNode, json.dumps({'portName':'iterations', 'dataType':'Integer', 'addMayaAttr': True}))

cmds.setAttr(influenceMushNode + '.iterations', 30);

cmds.fabricSplice('addKLOperator', influenceMushNode, '{"opName":"tubeCharacter_DeltaMush"}', """

require RiggingToolbox;

operator tubeCharacter_DeltaMush(
  io GeometryStack stack,
  Integer iterations
) {
  if(stack.numGeometryOperators() >= 3){
    DeltaMushModifier deltaMushModifier = stack.getGeometryOperator(2);
    deltaMushModifier.setNumIterations(iterations);
  }
}
""")

cmds.connectAttr(influencePoseNode + '.stack', influenceMushNode + '.stack')


##############################################
## Set up the eval/render node.

influenceEvalNode = cmds.createNode("spliceMayaNode", name = "tubeCharacter_Eval")

cmds.fabricSplice('addInputPort', influenceEvalNode, json.dumps({'portName':'stack', 'dataType':'GeometryStack', 'extension':'RiggingToolbox', 'addSpliceMayaAttr':True, 'autoInitObjects': False}))
cmds.fabricSplice('addOutputPort', influenceEvalNode, json.dumps({'portName':'eval', 'dataType':'Scalar', 'addMayaAttr': True}))

cmds.connectAttr(influenceMushNode + '.stack', influenceEvalNode + '.stack')

cmds.fabricSplice('addKLOperator', influenceEvalNode, '{"opName":"tubeCharacter_Eval"}', """

require RiggingToolbox;

operator tubeCharacter_Eval(
  io GeometryStack stack,
  Scalar eval
) {
  EvalContext context();
  stack.evaluate(context);

  //StopFabricProfiling();
  //report( GetEvalPathReport() );
  //report(stack.getDesc());
}
""")


##############################################
## Set up the loader node for the wraped geoms

wrappedGeomsInitNode = cmds.createNode("spliceMayaNode", name = "wrappedGeoms_Init")

cmds.fabricSplice('addInputPort', wrappedGeomsInitNode, json.dumps({'portName':'filePath', 'dataType':'String', 'addMayaAttr': True}))
cmds.fabricSplice('addOutputPort', wrappedGeomsInitNode, json.dumps({'portName':'stack', 'dataType':'GeometryStack', 'extension':'RiggingToolbox', 'addSpliceMayaAttr':True, 'autoInitObjects': True}))

cmds.setAttr(wrappedGeomsInitNode + '.filePath', "C:/Users/Phil/Projects/RiggingToolbox/Tests/GeometryStack/Resources/tubeCharacter_Wrap.json", type="string");


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
cmds.fabricSplice('addOutputPort', wrappedGeomsEvalNode, json.dumps({'portName':'eval', 'dataType':'Scalar', 'addMayaAttr': True}))

cmds.connectAttr(wrappedGeomsInitNode + '.stack', wrappedGeomsEvalNode + '.stack')
cmds.connectAttr(influenceEvalNode + '.stack', wrappedGeomsEvalNode + '.srcstack')

cmds.fabricSplice('addKLOperator', wrappedGeomsEvalNode, '{"opName":"wrappedGeoms_Eval"}', """

require RiggingToolbox;

operator wrappedGeoms_Eval(
  io GeometryStack stack,
  io GeometryStack srcstack,
  Scalar eval
) {
  if(stack.numGeometryOperators() >= 2){
    WrapModifier wrapModifier = stack.getGeometryOperator(1);
    wrapModifier.setSourceGeomStack(srcstack);
  }

  EvalContext context();
  stack.evaluate(context);

  //StopFabricProfiling();
  //report( GetEvalPathReport() );
  //report(stack.getDesc());
}
""")

##############################################
## Set up the eval locator.

forceEvalLocator = cmds.createNode("locator", name = "forceEval")
cmds.connectAttr(wrappedGeomsEvalNode + '.eval', forceEvalLocator + '.localPosition.localPositionY')
