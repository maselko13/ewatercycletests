from Test import Test
from TestResult import TestResult

def initializeWrongConfigCondition(model):
    # only path4 results in an actual .json file
    path = "this is not a path"
    path2 = "maybe/valid.json"
    path3 = "valid.json"
    path4 = "cfg.json"
    correct = 0
    try:
      model.initialize(path)
      model.initialize(path2)
      model.initialize(path3)
    except:
        correct = correct + 1
    if correct == 0 :
      return TestResult(False, "model initialized despite invalid path!")
    try:
        model.initialize(path4)
    except:
        return TestResult(False,"model throws exception on valid config file!")
    return TestResult(True)
def correctStartTimeCondition(model):
    if model.get_start_time() == 0.0:
        return TestResult(True)
    else:
        return TestResult(False,"Model start time is incorrect")
def timePassageCondition(model):
    number = model.get_current_time()
    model.update()
    if model.get_current_time() == number - model.get_time_step():
        return TestResult(True)
    else:
        return TestResult(False,"the model's time does not update properly")
def invalidGridTypeCondition(model):
    # list of all correct grid types as per the BMI specification
    valid_types = ['scalar', 'points', 'vector', 'unstructured', 'structured_quadrilateral', 'rectilinear',
                   'uniform_rectilinear']
    temp = 0
    while True:
        try:
            type = model.get_grid_type(temp)
            # use flag while iterating through the list to check if the type is valid
            flag = 0
            for valid in valid_types:
                if type == valid:
                    flag = 1
                    break
            if flag == 0:
              return TestResult(False,"The model's grid's type is invalid")
            else:
              flag = 0
            temp += 1
        except:
            return TestResult(True)
def invalidGridRankCondition(model):
    temp = 0
    while True:
        try:
            rank = model.get_grid_rank(temp)
            # you can't have 4 or more dimensional models, that's literally impossible
            if rank != 0 and rank != 1 and rank != 2 and rank != 3:
                return TestResult(False,"the model's grid's rank is invalid")
            temp += 1
        except:
            return TestResult(True)
def gridTypeMismatchCondition(model):
    temp = 0
    while True:
      try:
       type = model.get_grid_type(temp)
       rank = model.get_grid_rank(temp)
       # ifs used to check if grid types have correct dimensions
       if type == 'scalar' and rank!=0:
           return TestResult(False,"the model outputs wrong grid data!")
       if type == 'vector' and rank!=1:
           return TestResult(False, "the model outputs wrong grid data!")
       if type == 'structured_quadrilateral' and rank != 2:
          return TestResult(False, "the model outputs wrong grid data!")
       if type == 'rectilinear' and rank != 2:
          return TestResult(False, "the model outputs wrong grid data!")
       if type == 'uniform_rectilinear' and rank != 2:
          return TestResult(False, "the model outputs wrong grid data!")
       temp += 1
      except:
          return TestResult(True)
initializeWrongConfigTest = Test(name="InitializeWrongConfig", description="tests if the model can be initialized without a proper config file path", critical=True, enabled=True)
correctStartTimeTest = Test(name="CorrectStartTime", description="Checks if the start time of the model is correct", critical=False, enabled=True)
properTimePassageTest = Test(name="ProperTimePassage", description="tests if the time passes properly when the model is updated", critical=True, enabled=True)
invalidGridTypeTest = Test(name="InvalidGridType", description="tests if any of the model's grids have are of invalid type", critical=True, enabled=True)
invalidGridRankTest = Test(name="InvalidGridRank", description="tests if any of the model's grids have are of invalid rank", critical=True, enabled=True)
gridTypeMismatchTest = Test(name="GridTypeMismatch", description="tests if the rank of the model's grids matches their type", critical=True, enabled=True)
initializeWrongConfigTest.run = initializeWrongConfigCondition
correctStartTimeTest.run = correctStartTimeCondition
properTimePassageTest.run = timePassageCondition
invalidGridTypeTest.run = invalidGridTypeCondition
invalidGridRankTest.run = invalidGridRankCondition
gridTypeMismatchTest.run = gridTypeMismatchCondition
def addSpecTests(testSuite):
    testSuite.addTest(initializeWrongConfigTest)
    testSuite.addTest(correctStartTimeTest)
    testSuite.addTest(properTimePassageTest)
    testSuite.addTest(invalidGridTypeTest)
    testSuite.addTest(invalidGridRankTest)
    testSuite.addTest(gridTypeMismatchTest)
