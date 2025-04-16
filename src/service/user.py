import bcrypt
from jose import jwt
from datetime import datetime ,timedelta
class UserService:
    
    encoding : str = "UTF-8"
    secret_key : str = "4ae4e8064318ed1fed299f459210310e560492de439455856e94707ed7b10cfb"
    jwt_algorithm :str = "HS256"
    
    def hash_password(self , plain_password : str) ->str:
        hashed = bcrypt.hashpw(plain_password.encode(self.encoding) , salt=bcrypt.gensalt())
        return hashed.decode(self.encoding)
    
    
    def verify_password(
        self , plain_password : str , hashed_password : str
    ) -> bool :
        
        
        return bcrypt.checkpw(
            plain_password.encode(self.encoding),
            hashed_password.encode(self.encoding)
        )
        
        
    def create_jwt(self , username : str) -> str:
        return jwt.encode(
            {
                "sub" : username,
                "exp" : datetime.now() + timedelta(days=1)
            },
            self.secret_key,
            algorithm=self.jwt_algorithm,
            )