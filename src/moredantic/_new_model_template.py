# The only purpose of this file is to be copy pasted as a template when creating new model files to save time.  # noqa: E501
# The file is not intended to be used directly, that's why it doesn't have a specific name,
# nor is it exported anywhere and it's name is prefixed with an underscore.
# NOTES:
# - In regions _Internal Helper Methods sections, properties/cached_properties also apply if
#   logically they are not really properties but helper methods that make sense to be chached p.e..
# - In regions Normal Methods sections, properties/cached_properties also apply if
#   logically they are not really properties but methods that return callables, basically working as a function.  # noqa: E501



# ---> First party imports <--- #
from chatbot_app.mydantic import BaseModel


class NewModelTemplate(BaseModel):
  #region Model Config + Class Variables
  #endregion Model Config + Class Variables


  #region Instance Fields + Properties
  #endregion Instance Fields + Properties


  #region Init Subclass + Abstract Methods
  #endregion Init Subclass + Abstract Methods


  #region Class + Static Methods
  #region _Internal Helper Methods
  #endregion _Internal Helper Methods

  #region Normal Methods
  #endregion Normal Methods

  #region Custom Tool Methods
  #endregion Custom Tool Methods
  #endregion Class + Static Methods


  #region New + Init + Post Init + Validators Methods
  #endregion New + Init + Post Init + Validators Methods


  #region Instance Methods
  #region _Internal Helper Methods
  #endregion _Internal Helper Methods

  #region Normal Methods
  #endregion Normal Methods

  #region Custom Tool Methods
  pass
  #endregion Custom Tool Methods
  #endregion Instance Methods
