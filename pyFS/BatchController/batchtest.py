from batch_controller import BatchController
from commands import *

bc = BatchController('C:\Dev\pyFS\Model', 'test model')
c = Winfram('I')
bc.run_command(c)