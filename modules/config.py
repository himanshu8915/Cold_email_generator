class Config:
    def __init__(self, company_name, position, company_description, intention, email_purpose):
        self.company_name = company_name
        self.position = position
        self.company_description = company_description
        self.intention = intention
        self.email_purpose = email_purpose

    def get_config(self):
        return {
            "company_name": self.company_name,
            "position": self.position,
            "company_description": self.company_description,
            "intention": self.intention,
            "email_purpose": self.email_purpose
        }
