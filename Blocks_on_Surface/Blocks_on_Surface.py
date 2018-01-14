import string
from sys import exit
import NXOpen
import NXOpen.BlockStyler
import NXOpen.Features
import NXOpen.UF
import NXOpen.GeometricAnalysis
import NXOpen.Facet
import NXOpen.GeometricUtilities



class blocks:
    # static class members
    theSession = None
    theUI = None
    
    #------------------------------------------------------------------------------
    # Constructor for NX Styler class
    #------------------------------------------------------------------------------
    def __init__(self):
        try:
            self.theSession = NXOpen.Session.GetSession()
            self.theUI = NXOpen.UI.GetUI()
            self.theDlxFileName = "blocks.dlx"
            self.theDialog = self.theUI.CreateDialog(self.theDlxFileName)
            self.theDialog.AddApplyHandler(self.apply_cb)
            self.theDialog.AddOkHandler(self.ok_cb)
            self.theDialog.AddCancelHandler(self.cancel_cb)
            self.theDialog.AddUpdateHandler(self.update_cb)
            self.theDialog.AddInitializeHandler(self.initialize_cb)
            self.theDialog.AddDialogShownHandler(self.dialogShown_cb)


        except Exception as ex:
            # ---- Enter your exception handling code here -----
            raise ex
        

    def Show(self):
        try:
            self.theDialog.Show()
        except Exception as ex:
            # ---- Enter your exception handling code here -----
            self.theUI.NXMessageBox.Show("Block Styler", NXOpen.NXMessageBox.DialogType.Error, str(ex))
        
    



    #------------------------------------------------------------------------------
    # Method Name: Dispose
    #------------------------------------------------------------------------------
    def Dispose(self):
        if self.theDialog != None:
            self.theDialog.Dispose()
            self.theDialog = None
  
    #------------------------------------------------------------------------------
    # Callback Name: initialize_cb
    #------------------------------------------------------------------------------
    def initialize_cb(self):
        try:
            self.faace = self.theDialog.TopBlock.FindBlock("faace")
            self.num_of_blocks = self.theDialog.TopBlock.FindBlock("num_of_blocks")
            self.block_size = self.theDialog.TopBlock.FindBlock("block_size")
            self.group0 = self.theDialog.TopBlock.FindBlock("group0")
        except Exception as ex:
            # ---- Enter your exception handling code here -----
            self.theUI.NXMessageBox.Show("Block Styler", NXOpen.NXMessageBox.DialogType.Error, str(ex))
        
    def cancel_cb(self):
     
        try:
            global NEW_LIST
            NEW_LIST = [1 ] 
        except Exception as ex:
            # ---- Enter your exception handling code here -----
            self.theUI.NXMessageBox.Show("Block Styler", NXOpen.NXMessageBox.DialogType.Error, str(ex))


   
    def dialogShown_cb(self):
        try:
            # ---- Enter your callback code here -----
            pass
        except Exception as ex:
            # ---- Enter your exception handling code here -----
            self.theUI.NXMessageBox.Show("Block Styler", NXOpen.NXMessageBox.DialogType.Error, str(ex))
        
    
    #------------------------------------------------------------------------------
    # Callback Name: apply_cb
    #------------------------------------------------------------------------------
    def apply_cb(self):
        errorCode = 0
        try:
            # ---- Enter your callback code here -----
            pass
        except Exception as ex:
            # ---- Enter your exception handling code here -----
            errorCode = 1
            self.theUI.NXMessageBox.Show("Block Styler", NXOpen.NXMessageBox.DialogType.Error, str(ex))
        
        return errorCode
    
    #------------------------------------------------------------------------------
    # Callback Name: update_cb
    #------------------------------------------------------------------------------
    def update_cb(self, block):
        try:
            if block == self.faace:
                # ---- Enter your code here -----
                pass
            elif block == self.num_of_blocks:
                # ---- Enter your code here -----
                pass
            elif block == self.block_size:
                # ---- Enter your code here -----
                pass
        except Exception as ex:
            # ---- Enter your exception handling code here -----
            self.theUI.NXMessageBox.Show("Block Styler", NXOpen.NXMessageBox.DialogType.Error, str(ex))
        
        return 0
    
    #------------------------------------------------------------------------------
    # Callback Name: ok_cb
    #------------------------------------------------------------------------------
    def ok_cb(self):
        errorCode = 0
        try:
            global NEW_LIST
            NEW_LIST = [self.num_of_blocks.Value, self.faace.GetSelectedObjects() , self.block_size.Value ] 
            # ---- Enter your callback code here -----
            errorCode = self.apply_cb()
        except Exception as ex:
            # ---- Enter your exception handling code here -----
            errorCode = 1
            self.theUI.NXMessageBox.Show("Block Styler", NXOpen.NXMessageBox.DialogType.Error, str(ex))
        
        return errorCode




    
    
    #------------------------------------------------------------------------------
    # Function Name: GetBlockProperties
    # Returns the propertylist of the specified BlockID
    #------------------------------------------------------------------------------
    def GetBlockProperties(self, blockID):
        try:
            return self.theDialog.GetBlockProperties(blockID)
        except Exception as ex:
            # ---- Enter your exception handling code here -----
            self.theUI.NXMessageBox.Show("Block Styler", NXOpen.NXMessageBox.DialogType.Error, str(ex))
        
        return None
    
def main_styl():
    global NEW_LIST
    theblocks = None
    try:
        theblocks =  blocks()
        #  The following method shows the dialog immediately
        theblocks.Show()
        return NEW_LIST
    except Exception as ex:
        # ---- Enter your exception handling code here -----
        NXOpen.UI.GetUI().NXMessageBox.Show("Block Styler", NXOpen.NXMessageBox.DialogType.Error, str(ex))
    finally:
        if theblocks != None:
            theblocks.Dispose()
            theblocks = None
 

def main_first(new_list):


    if new_list.count(1) == 1:
        return
    theSession = NXOpen.Session.GetSession()
    theUI = NXOpen.UI.GetUI()
    
    global theMessageBox 
    theMessageBox = theUI.NXMessageBox
    undoMark = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Blank")
    
    workPart= theSession.Parts.Work

    selectManager = theUI.SelectionManager
    nums_of_selected = selectManager.GetNumSelectedObjects()

    #if nums_of_selected > 1:
    #    theMessageBox.Show(
    #    "Selection Error", NXOpen.NXMessageBox.DialogType.Information,
    #    "Too much objects selected :  %d " % (nums_of_selected ) )
    #    return
   
    #if nums_of_selected < 1:
    #    theMessageBox.Show(
    #    "Selection Error", NXOpen.NXMessageBox.DialogType.Information,
    #    "No objects selected " )
    #    return    

    #selectrd_obj = selectManager.GetSelectedTaggedObject(0)    
    selectrd_obj = new_list[1][0]
    body = workPart.Bodies.FindObject(selectrd_obj.JournalIdentifier)
    bf = body.GetFeatures()
    extrude_feature = bf[0]

    ext_parents = extrude_feature.GetParents()
    spline = ext_parents[0]
    name = spline.FeatureType

    ex_build = workPart.Features.CreateExtrudeBuilder(extrude_feature)
    face1 = extrude_feature.GetFaces()
   

    num_of_box_in_line = new_list[0]
    size_of_cube = new_list[2]

    
    global  first, sec ,thir
    first = sec = thir = 1
    byX = 1 / (num_of_box_in_line+1)
    byY = 1 / (num_of_box_in_line+1)



    byX1= byX
    byY1= byY
    for i in range(num_of_box_in_line):
        for j in range(num_of_box_in_line):
            cre_bl(workPart,face1[0], byX1, byY1, size_of_cube)
            byY1 = byY1+ byY
        byX1 = byX1+ byX
        byY1= byY

def cre_bl(workPart , face, byX,byY, size_bl ):
    global theMessageBox 
    global  first, sec ,thir
    scalar1 = workPart.Scalars.CreateScalar(byX, NXOpen.Scalar.DimensionalityType.NotSet, NXOpen.SmartObject.UpdateOption.WithinModeling)
    scalar2 = workPart.Scalars.CreateScalar(byY, NXOpen.Scalar.DimensionalityType.NotSet, NXOpen.SmartObject.UpdateOption.WithinModeling)
    point1 = workPart.Points.CreatePoint(face, scalar1, scalar2, NXOpen.SmartObject.UpdateOption.WithinModeling)
    originPoint1 = NXOpen.Point3d(1000.0, 1000.0, 1000.0)
    direc = workPart.Directions.CreateDirection(point1,face, NXOpen.DirectionOnFaceOption.Normal, NXOpen.SmartObject.Null ,NXOpen.Sense.Forward , NXOpen.SmartObjectUpdateOption.WithinModeling)   
    xAxisss= direc.Vector


    targetBodies1 = [NXOpen.Body.Null] * 1 
    targetBodies1[0] = NXOpen.Body.Null
    block = NXOpen.Features.Feature.Null
    BlockfeatBuilder = workPart.Features.CreateBlockFeatureBuilder(block)
    BlockfeatBuilder.SetBooleanOperationAndTarget(NXOpen.Features.FeatureBooleanType.Create , targetBodies1[0])
    BlockfeatBuilder.OriginPoint = point1
    BlockfeatBuilder.SetOriginAndLengths( originPoint1 , str(size_bl) , str(size_bl) ,str(size_bl))
     
    
    if (abs(xAxisss.X)  < 0.001 and first ):
        sec = 0
        thir = 0
        Y = 1.0
        X = 0.0
        BlockfeatBuilder.SetOrientation(   NXOpen.Vector3d( X , Y,  -( xAxisss.Y +  xAxisss.X)/xAxisss.Z ) , xAxisss)
    elif (abs(xAxisss.Y  )< 0.001 and sec):
        thir = 0
        first = 0
        Y = 0.0
        Z = 1.0
        BlockfeatBuilder.SetOrientation(   NXOpen.Vector3d(  -( xAxisss.Y +  xAxisss.Z)/xAxisss.X , Y , Z) , xAxisss)
    elif (abs(xAxisss.Z ) < 0.001 and thir ):
        first = 0
        sec = 0
        X = 1.0
        Z = 0.0
        BlockfeatBuilder.SetOrientation(   NXOpen.Vector3d( X,  -( xAxisss.X +  xAxisss.Z)/xAxisss.Y , Z) , xAxisss)
  
       
    BlockfeatBuilder.CommitFeature()   


   
if __name__ == '__main__':
    main_first( main_styl())

