
import json
from maya import cmds

import os
if 'FABRIC_RIGGINGTOOLBOX_PATH' not in os.environ:
  raise Exception("Please set the rigging ")
toolboxPath = os.environ['FABRIC_RIGGINGTOOLBOX_PATH']

cmds.file(new=True,f=True)


##############################################
## Set up the loader node.

initnode = cmds.createNode("spliceMayaNode", name = "tubeCharacter_Init")

cmds.fabricSplice('addInputPort', initnode, json.dumps({'portName':'filePath', 'dataType':'String', 'addMayaAttr': True}))
cmds.fabricSplice('addOutputPort', initnode, json.dumps({'portName':'stack', 'dataType':'GeometryStack', 'extension':'RiggingToolbox', 'addSpliceMayaAttr':True, 'autoInitObjects': True}))

cmds.setAttr(initnode + '.filePath', toolboxPath+"/Tests/GeometryStack/Resources/tubeCharacter_Loading.json", type="string");


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
## Set up the eval/render node.

evalStackNode = cmds.createNode("spliceMayaNode", name = "tubeCharacter_Eval")

cmds.fabricSplice('addInputPort', evalStackNode, json.dumps({'portName':'stack', 'dataType':'GeometryStack', 'extension':'RiggingToolbox', 'addSpliceMayaAttr':True, 'autoInitObjects': False}))
cmds.fabricSplice('addOutputPort', evalStackNode, json.dumps({'portName':'eval', 'dataType':'Scalar', 'addMayaAttr': True}))
cmds.fabricSplice('addInputPort', evalStackNode, json.dumps({'portName':'displayGeometries', 'dataType':'Boolean', 'addMayaAttr': True}))
cmds.setAttr(evalStackNode + '.displayGeometries', 1)


cmds.connectAttr(initnode + '.stack', evalStackNode + '.stack')

cmds.fabricSplice('addKLOperator', evalStackNode, '{"opName":"tubeCharacter_Eval"}', """

require RiggingToolbox;

operator tubeCharacter_Eval(
  io GeometryStack stack,
  Boolean displayGeometries,
  EvalContext context,
  Scalar eval
) {
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
