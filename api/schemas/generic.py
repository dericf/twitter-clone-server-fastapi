# Standard Library
from datetime import datetime, date

# Types
from typing import List, Optional, Any
from pydantic import BaseModel, validator

class EmptyResponse(BaseModel):
	"""Empty HTTP Respone (No Data)
	"""
	pass