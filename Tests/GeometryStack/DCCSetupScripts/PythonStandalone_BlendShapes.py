
cmds.newScene()

cmds.addPort(portName='filePath', dataType ='String', portType ='In' )
cmds.addPort(portName='stack', dataType ='GeometryStack', portType ='IO', extension='RiggingToolbox' )
cmds.addPort(portName='shape0', dataType ='Scalar', portType ='In', Range = { 'min': 0, 'max': 1.0 } )
cmds.addPort(portName='shape1', dataType ='Scalar', portType ='In', Range = { 'min': 0, 'max': 1.0 } )

cmds.addOperator(operatorName='blendShapesSphereCharacter', sourceCode="""

require RiggingToolbox;

operator blendShapesSphereCharacter(
  String filePath,
  io GeometryStack stack,
  Scalar shape0,
  Scalar shape1,
) {
  if(filePath != "" && stack.getFilePath() != filePath){
    report("filePath:" + filePath);
    stack.loadJSONFile(filePath);
    report("stack:" + stack.getDesc());
  }
  if(stack.numGeometryOperators() > 0){
    StartFabricProfiling();
    BlendShapesModifier blendShapesModifier = stack.getGeometryOperator(1);

    // Modify the pose and then reevaluate. 
    Scalar weights[];
    weights.resize(2);
    weights[0] = shape0;
    weights[1] = shape1;
    blendShapesModifier.setBlendWeights(weights);

    EvalContext context();
    stack.evaluate(context);

    StopFabricProfiling();

    report( GetEvalPathReport() );

  }
}
""")


cmds.setPortValue(portName='filePath', value="C:/Users/Phil/Projects/RiggingToolbox/Tests/GeometryStack/blendShapesSphereCharacter.json")
