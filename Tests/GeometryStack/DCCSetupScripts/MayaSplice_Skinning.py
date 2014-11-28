
import json
from maya import cmds

cmds.file(new=True,f=True)
cmds.file("C:/Users/Phil/Projects/RiggingToolbox/Tests/GeometryStack/Resources/SkinnedTube_hierarchy.ma", r=True);


##############################################
## Set up the loader node.

initnode = cmds.createNode("spliceMayaNode", name = "tubeCharacter_Init")

cmds.fabricSplice('addInputPort', initnode, json.dumps({'portName':'filePath', 'dataType':'String', 'addMayaAttr': True}))
cmds.fabricSplice('addOutputPort', initnode, json.dumps({'portName':'stack', 'dataType':'GeometryStack', 'extension':'RiggingToolbox', 'addSpliceMayaAttr':True, 'autoInitObjects': True}))

cmds.setAttr(initnode + '.filePath', "C:/Users/Phil/Projects/RiggingToolbox/Tests/GeometryStack/Resources/tubeCharacter_Skinning.json", type="string");


cmds.fabricSplice('addKLOperator', initnode, '{"opName":"tubeCharacter_Init"}', """

require RiggingToolbox;

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

poseNode = cmds.createNode("spliceMayaNode", name = "tubeCharacter_SetPose")

cmds.fabricSplice('addIOPort', poseNode, json.dumps({'portName':'stack', 'dataType':'GeometryStack', 'extension':'RiggingToolbox', 'addSpliceMayaAttr':True, 'autoInitObjects': False }))
cmds.fabricSplice('addInputPort', poseNode, json.dumps({'portName':'deformers', 'dataType':'Mat44[]', 'addMayaAttr': True, 'arrayType':"Array (Multi)"}))

cmds.connectAttr('SkinnedTube_hierarchy_joint1.worldMatrix[0]', poseNode + '.deformers[0]')
cmds.connectAttr('SkinnedTube_hierarchy_joint2.worldMatrix[0]', poseNode + '.deformers[1]')
cmds.connectAttr('SkinnedTube_hierarchy_joint3.worldMatrix[0]', poseNode + '.deformers[2]')
cmds.connectAttr('SkinnedTube_hierarchy_joint4.worldMatrix[0]', poseNode + '.deformers[3]')

cmds.fabricSplice('addKLOperator', poseNode, '{"opName":"tubeCharacter_SetPose"}', """

require RiggingToolbox;

operator tubeCharacter_SetPose(
  io GeometryStack stack,
  Mat44 deformers[]
) {
  if(stack.numGeometryOperators() >= 2){
    SkinningModifier skinningModifier = stack.getGeometryOperator(1);
    skinningModifier.setPose(deformers);
  }
}
""")

cmds.connectAttr(initnode + '.stack', poseNode + '.stack')


##############################################
## Set up the eval/render node.

evalStackNode = cmds.createNode("spliceMayaNode", name = "tubeCharacter_Eval")

cmds.fabricSplice('addInputPort', evalStackNode, json.dumps({'portName':'stack', 'dataType':'GeometryStack', 'extension':'RiggingToolbox', 'addSpliceMayaAttr':True, 'autoInitObjects': False}))
cmds.fabricSplice('addOutputPort', evalStackNode, json.dumps({'portName':'eval', 'dataType':'Scalar', 'addMayaAttr': True}))
cmds.fabricSplice('addInputPort', evalStackNode, json.dumps({'portName':'displayGeometries', 'dataType':'Boolean', 'addMayaAttr': True}))


cmds.connectAttr(poseNode + '.stack', evalStackNode + '.stack')

cmds.fabricSplice('addKLOperator', evalStackNode, '{"opName":"tubeCharacter_Eval"}', """

require RiggingToolbox;

operator tubeCharacter_Eval(
  io GeometryStack stack,
  Boolean displayGeometries,
  Scalar eval
) {
  stack.setDisplayGeometries(displayGeometries);

  EvalContext context();
  stack.evaluate(context);
}
""")


##############################################
## Set up the eval locator.

forceEvalLocator = cmds.createNode("locator", name = "forceEval")
cmds.connectAttr(evalStackNode + '.eval', forceEvalLocator + '.localPosition.localPositionY')
