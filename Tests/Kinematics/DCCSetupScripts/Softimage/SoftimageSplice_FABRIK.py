
import textwrap

def splice(operator, command, *args, **kwargs):
    return Application.fabricSplice(command, operator, str(kwargs), *args)


def set_kl(operator, op_name, code):
    splice(operator, "addKLOperator", opName=op_name)
    splice(operator, "setKLOperatorCode", code, opName=op_name)


base_pose = """
[
{
    "ori": {
        "v": {
            "x": -0.122267944616,
            "y": 0.221731002236,
            "z": -0.346426531163
        },
        "w": -0.346426531163
    },
    "tr": {
        "x": -11.4606533051,
        "y": -1.1777023077,
        "z": 9.64807033539
    },
    "sc": {
        "x": 0.99999998903,
        "y": 0.999999986678,
        "z": 0.999999994857
    }
},
{
    "ori": {
        "v": {
            "x": 0.22107035862,
            "y": 0.398678409024,
            "z": 0.626367216013
        },
        "w": 0.626367216013
    },
    "tr": {
        "x": -6.31690168381,
        "y": -6.46448326111,
        "z": 7.19262981415
    },
    "sc": {
        "x": 1.00000002489,
        "y": 1.0000000116,
        "z": 1.00000002151
    }
},
{
    "ori": {
        "v": {
            "x": -0.14991666643,
            "y": 0.188954085851,
            "z": -0.424764713563
        },
        "w": -0.424764713563
    },
    "tr": {
        "x": -7.70380449295,
        "y": 6.6312122345,
        "z": 4.11952924728
    },
    "sc": {
        "x": 1.00000000534,
        "y": 1.00000000428,
        "z": 0.999999984937
    }
},
{
    "ori": {
        "v": {
            "x": -0.227786421098,
            "y": 0.0751234671516,
            "z": -0.64539612401
        },
        "w": -0.64539612401
    },
    "tr": {
        "x": -4.1147441864,
        "y": 1.58694446087,
        "z": 2.84005212784
    },
    "sc": {
        "x": 1.00000000913,
        "y": 1.00000000803,
        "z": 0.999999992899
    }
},
{
    "ori": {
        "v": {
            "x": -0.0726328089391,
            "y": 0.273018664355,
            "z": -0.20579335443
        },
        "w": -0.20579335443
    },
    "tr": {
        "x": -2.55877375603,
        "y": -8.11357021332,
        "z": 4.69017314911
    },
    "sc": {
        "x": 0.999999982221,
        "y": 0.999999992532,
        "z": 1.00000003018
    }
},
{
    "ori": {
        "v": {
            "x": 0.135055690298,
            "y": 0.397659323137,
            "z": 0.382658535497
        },
        "w": 0.382658535497
    },
    "tr": {
        "x": 9.23816776276,
        "y": -14.6614189148,
        "z": -2.72626614571
    },
    "sc": {
        "x": 0.999999972694,
        "y": 0.999999963491,
        "z": 1.0000000191
    }
},
{
    "ori": {
        "v": {
            "x": 0.135055691827,
            "y": 0.397659318996,
            "z": 0.382658539503
        },
        "w": 0.382658539503
    },
    "tr": {
        "x": 13.5832733885,
        "y": -6.46643616064,
        "z": -8.8526959585
    },
    "sc": {
        "x": 1.0,
        "y": 1.0,
        "z": 1.0
    }
},
]
"""
klCode = textwrap.dedent("""


require Xfo;
require Mat44;

require RiggingToolbox;


operator myCustomConstraint(io Xfo base_pose[], io Scalar bone_length, io FABRIKSolver fabrik, in Mat44 ik_handle, io Mat44 output[] ) {

  Vec3 goal();
  Xfo ikpose[];

  if (fabrik.num_bones == 0) {
    fabrik = FABRIKSolver( base_pose );
  }

  fabrik.EvaluateBoneTransforms( output, Xfo(ik_handle).tr );
}
""")


Application.GetPrim("Bone", "", "Scene_Root", "")
Application.Translate("", -11.4606535852798, -1.17770225881107, 9.64807039296736, "siAbsolute", "siLocal", "siObj", "siXYZ", "", "", "siXYZ", "", "", "", "", "", "", 0, "")
Application.Rotate("", -23.2479590782778, 18.4119407181975, -45.785621539382, "siAbsolute", "siLocal", "siObj", "siXYZ", "", "", "", "", "", "", "", 0, "")
Application.SetValue(".length", 7.77415079054298, "")
Application.GetPrim("Bone", "", "bone", "")
Application.Translate("", 7.77415079054298, 1.33226762955019E-15, -8.88178419700125E-16, "siAbsolute", "siLocal", "siObj", "siXYZ", "", "", "siXYZ", "", "", "", "", "", "", 0, "")
Application.Rotate("", 23.25446240029, 10.5303161512379, 131.74879371648, "siAbsolute", "siLocal", "siObj", "siXYZ", "", "", "", "", "", "", "", 0, "")
Application.SetValue(".length", 13.5227469991095, "")
Application.GetPrim("Bone", "", "bone1", "")
Application.Translate("", 13.5227469991095, 0, -4.44089209850063E-16, "siAbsolute", "siLocal", "siObj", "siXYZ", "", "", "siXYZ", "", "", "", "", "", "", 0, "")
Application.Rotate("", 25.0567216880896, -8.61416632968262, -142.554016481869, "siAbsolute", "siLocal", "siObj", "siXYZ", "", "", "", "", "", "", "", 0, "")
Application.SetValue(".length", 6.32163405542311, "")
Application.GetPrim("Bone", "", "bone2", "")
Application.Translate("", 6.32163405542311, 2.22044604925031E-16, 4.44089209850063E-16, "siAbsolute", "siLocal", "siObj", "siXYZ", "", "", "siXYZ", "", "", "", "", "", "", 0, "")
Application.Rotate("", 2.3728769542166, -7.84940385198699, -33.5950290984295, "siAbsolute", "siLocal", "siObj", "siXYZ", "", "", "", "", "", "", "", 0, "")
Application.SetValue(".length", 9.99719885922297, "")
Application.GetPrim("Bone", "", "bone3", "")
Application.Translate("", 9.99719885922297, 0, 0, "siAbsolute", "siLocal", "siObj", "siXYZ", "", "", "siXYZ", "", "", "", "", "", "", 0, "")
Application.Rotate("", 7.69523182816763, 12.5195200478413, 63.0276798209404, "siAbsolute", "siLocal", "siObj", "siXYZ", "", "", "", "", "", "", "", 0, "")
Application.SetValue(".length", 15.3962891241979, "")
Application.GetPrim("Bone", "", "bone4", "")
Application.Translate("", 15.3962891241979, 2.33146835171283E-15, 4.44089209850063E-16, "siAbsolute", "siLocal", "siObj", "siXYZ", "", "", "siXYZ", "", "", "", "", "", "", 0, "")
Application.Rotate("", 10.405685413798, 13.5323706166991, 75.0110737280288, "siAbsolute", "siLocal", "siObj", "siXYZ", "", "", "", "", "", "", "", 0, "")
Application.SetValue(".length", 10.9873057658091, "")
Application.ActivateSelectTool()
Application.SetAndToggleSelection("bone5", "", True)
Application.ActivateSelectTool()



Application.GetPrim("Null", "", "", "")
Application.GetPrim("Null", "", "", "")
Application.DeselectAll()

Application.ParentObj("B:bone5", "null")
Application.DeselectAll()

Application.ActivateSelectTool()
Application.SetAndToggleSelection("null", "", True)
Application.ActivateSelectTool()
Application.Rotate("", 0, 0, 0, "siAbsolute", "siParent", "siObj", "siX", "", "", "", "", "", "", "", 0, "")
Application.Rotate("", 0, 0, 0, "siAbsolute", "siParent", "siObj", "siY", "", "", "", "", "", "", "", 0, "")
Application.Rotate("", 0, 0, 0, "siAbsolute", "siParent", "siObj", "siZ", "", "", "", "", "", "", "", 0, "")
Application.Translate("", 0, 0, 0, "siAbsolute", "siParent", "siObj", "siX", "", "", "", "", "", "", "", "", "", 0, "")
Application.Translate("", 0, 0, 0, "siAbsolute", "siParent", "siObj", "siY", "", "", "", "", "", "", "", "", "", 0, "")
Application.Translate("", 0, 0, 0, "siAbsolute", "siParent", "siObj", "siZ", "", "", "", "", "", "", "", "", "", 0, "")
Application.Translate("", 11.1162411669007, 0, 0, "siRelative", "siParent", "siObj", "siXYZ", "", "", "", "", "", "", "", "", "", 0, "")
Application.CutObj("")

op = Application.fabricSplice("newSplice", '{"targets":"bone.kine.global,bone1.kine.global,bone2.kine.global,bone3.kine.global,bone4.kine.global,bone5.kine.global,null1.kine.global","portName":"output","portMode":"io"}')
splice(op, "addInputPort",    portName="ik_handle",   dataType="Mat44",   targets="null.kine.global")
splice(op, "addInternalPort", portName="base_pose",   dataType="Xfo[]",   portMode="IO", extension="")
splice(op, "addInternalPort", portName="bone_length", dataType="Scalar",  portMode="IO", extension="")
Application.fabricSplice("addInternalPort", "bone.kine.global.SpliceOp", "{\"portName\":\"fabrik\", \"dataType\":\"FABRIKSolver\", \"extension\":\"RiggingToolbox\", \"portMode\":\"IO\"}", "")
Application.fabricSplice('setPortData', op, '{"portName":"base_pose"}', base_pose);
#set_kl(op, "myCustomConstraint", "")
set_kl(op, "myCustomConstraint", klCode)
