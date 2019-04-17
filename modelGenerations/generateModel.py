from imageGeneration.generateImage import create_image
from pxr import Usd, UsdGeom, UsdShade, Sdf, Gf, Kind


def generate_chart_model(stage, index, stock_name, prices, percentage_change):
    stage = generate_ticker_cube(index, stage, stock_name)

    for i in range(0, len(prices)):
        mesh = UsdGeom.Mesh.Define(stage, '/cube' + str(i) + stock_name)
        mesh.CreateSubdivisionSchemeAttr().Set(UsdGeom.Tokens.none)
        mesh.CreatePointsAttr(
            [(-5, -5, 5), (5, -5, 5), (-5, prices[i], 5), (5, prices[i], 5), (-5, prices[i], -5),
             (5, prices[i], -5), (-5, -5, -5),
             (5, -5, -5)])
        mesh.CreateExtentAttr(UsdGeom.PointBased(mesh).ComputeExtent(mesh.GetPointsAttr().Get()))
        mesh.CreateNormalsAttr([(0, 0, 1), (0, 1, 0), (0, 0, -1), (0, -1, 0), (1, 0, 0), (-1, 0, 0)])
        mesh.SetNormalsInterpolation(UsdGeom.Tokens.uniform)

        mesh.CreateFaceVertexCountsAttr([4, 4, 4, 4, 4, 4])
        mesh.CreateFaceVertexIndicesAttr([0, 1, 3, 2, 2, 3, 5, 4, 4, 5, 7, 6, 6, 7, 1, 0, 1, 7, 5, 3, 6, 0, 2, 4])

        material = UsdShade.Material.Define(stage, '/cubeMaterial' + str(i) + stock_name)
        pbrShader = UsdShade.Shader.Define(stage,
                                           '/cubeMaterial' + str(i) + stock_name + '/PBRShader')

        pbrShader.CreateIdAttr('UsdPreviewSurface')
        if percentage_change[i] >= 0:
            pbrShader.CreateInput('diffuseColor', Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(0, 1, 0))
        else:
            pbrShader.CreateInput('diffuseColor', Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(1, 0, 0))
        pbrShader.CreateInput('metallic', Sdf.ValueTypeNames.Float).Set(0.9)
        pbrShader.CreateInput('roughness', Sdf.ValueTypeNames.Float).Set(0.2)
        material.CreateSurfaceOutput().ConnectToSource(pbrShader, 'surface')
        UsdShade.MaterialBindingAPI(mesh.GetPrim()).Bind(material)
        UsdGeom.XformCommonAPI(mesh).SetTranslate((10 * i, 20 * index, - index * 20))
        generate_price_cube(prices[i], stock_name, stage, i, index)


def generate_ticker_cube(index, stage, stock_name):
    stage.SetStartTimeCode(0)
    stage.SetEndTimeCode(192)
    TextureRoot = UsdGeom.Xform.Define(stage, '/TexModel' + stock_name)
    Usd.ModelAPI(TextureRoot).SetKind(Kind.Tokens.component)

    billboard = UsdGeom.Mesh.Define(stage, "/TexModel" + stock_name + "/card" + stock_name)
    billboard.CreatePointsAttr([(-5, -5, 5), (5, -5, 5), (5, 5, 5), (-5, 5, 5)])
    billboard.CreateFaceVertexCountsAttr([4])
    billboard.CreateFaceVertexIndicesAttr([0, 1, 2, 3])
    billboard.CreateExtentAttr([(-5, -5, 5), (5, 5, 5)])
    texCoords = billboard.CreatePrimvar("st",
                                        Sdf.ValueTypeNames.TexCoord2fArray,
                                        UsdGeom.Tokens.varying)
    texCoords.Set([(0, 0), (1, 0), (1, 1), (0, 1)])

    material = UsdShade.Material.Define(stage, '/TexModel' + stock_name + '/boardMat' + stock_name)
    stInput = material.CreateInput('frame:stPrimvarName', Sdf.ValueTypeNames.Token)
    stInput.Set('st')
    pbrShader = UsdShade.Shader.Define(stage, '/TexModel' + stock_name + '/boardMat/PBRShader' + stock_name)
    pbrShader.CreateIdAttr("UsdPreviewSurface")
    pbrShader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.4)
    pbrShader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)

    material.CreateSurfaceOutput().ConnectToSource(pbrShader, "surface")
    stReader = UsdShade.Shader.Define(stage, '/TexModel' + stock_name + '/boardMat/stReader' + stock_name)
    stReader.CreateIdAttr('UsdPrimvarReader_float2')

    stReader.CreateInput('varname', Sdf.ValueTypeNames.Token).ConnectToSource(stInput)
    print(stock_name)
    diffuseTextureSampler = UsdShade.Shader.Define(stage,
                                                   '/TexModel' + stock_name + '/boardMat/diffuseTexture' + stock_name)
    diffuseTextureSampler.CreateIdAttr('UsdUVTexture')
    diffuseTextureSampler.CreateInput('file', Sdf.ValueTypeNames.Asset).Set(
        '/Users/Abhinav/Documents/USDZ/CNBC/textures/' + stock_name + '.png')
    diffuseTextureSampler.CreateInput("st", Sdf.ValueTypeNames.Float2).ConnectToSource(stReader, 'result')
    diffuseTextureSampler.CreateOutput('rgb', Sdf.ValueTypeNames.Float3)
    pbrShader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).ConnectToSource(diffuseTextureSampler, 'rgb')
    UsdShade.MaterialBindingAPI(billboard.GetPrim()).Bind(material)
    UsdGeom.XformCommonAPI(billboard).SetTranslate((-20, 20 * index, - index * 20))
    spin = billboard.AddRotateYOp(opSuffix='spin')
    spin.Set(time=0, value=0)
    spin.Set(time=192, value=1440)
    return stage


def generate_price_cube(price, stock_name, stage, position, index):
    path = create_image(price, stock_name,position)
    TextureRoot = UsdGeom.Xform.Define(stage, '/priceModel' + stock_name + str(position))
    Usd.ModelAPI(TextureRoot).SetKind(Kind.Tokens.component)

    billboard = UsdGeom.Mesh.Define(stage,
                                    "/priceModel" + stock_name + str(position) + "/card" + stock_name + str(position))
    billboard.CreatePointsAttr([(-5, -5, 5), (5, -5, 5), (5, 5, 5), (-5, 5, 5)])
    billboard.CreateFaceVertexCountsAttr([4])
    billboard.CreateFaceVertexIndicesAttr([0, 1, 2, 3])
    billboard.CreateExtentAttr([(-5, -5, 5), (5, 5, 5)])
    texCoords = billboard.CreatePrimvar("st",
                                        Sdf.ValueTypeNames.TexCoord2fArray,
                                        UsdGeom.Tokens.varying)
    texCoords.Set([(0, 0), (1, 0), (1, 1), (0, 1)])

    material = UsdShade.Material.Define(stage,
                                        '/priceModel' + stock_name + str(position) + '/boardMat' + stock_name + str(
                                            position))
    stInput = material.CreateInput('frame:stPrimvarName', Sdf.ValueTypeNames.Token)
    stInput.Set('st')
    pbrShader = UsdShade.Shader.Define(stage,
                                       '/priceModel' + stock_name + str(
                                           position) + '/boardMat/PBRShader' + stock_name + str(position))
    pbrShader.CreateIdAttr("UsdPreviewSurface")
    pbrShader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.4)
    pbrShader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)

    material.CreateSurfaceOutput().ConnectToSource(pbrShader, "surface")
    stReader = UsdShade.Shader.Define(stage, '/priceModel' + stock_name + str(
        position) + '/boardMat/stReader' + stock_name + str(position))
    stReader.CreateIdAttr('UsdPrimvarReader_float2')

    stReader.CreateInput('varname', Sdf.ValueTypeNames.Token).ConnectToSource(stInput)
    diffuseTextureSampler = UsdShade.Shader.Define(stage,
                                                   '/priceModel' + stock_name + str(
                                                       position) + '/boardMat/diffuseTexture' + stock_name + str(
                                                       position))
    diffuseTextureSampler.CreateIdAttr('UsdUVTexture')
    diffuseTextureSampler.CreateInput('file', Sdf.ValueTypeNames.Asset).Set(path)
    diffuseTextureSampler.CreateInput("st", Sdf.ValueTypeNames.Float2).ConnectToSource(stReader, 'result')
    diffuseTextureSampler.CreateOutput('rgb', Sdf.ValueTypeNames.Float3)
    pbrShader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).ConnectToSource(diffuseTextureSampler, 'rgb')
    UsdShade.MaterialBindingAPI(billboard.GetPrim()).Bind(material)
    UsdGeom.XformCommonAPI(billboard).SetTranslate((10 * position, (20 * index) + (price + 5), - index * 20))
