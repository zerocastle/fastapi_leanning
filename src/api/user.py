
from fastapi import APIRouter , Depends , HTTPException
from schema.request import SignUpRequest , Login_by_user
from schema.response import UserShema , JWTResponse
from service.user import UserService
from database.repository import UserRepository
from database.orm import User

router = APIRouter(prefix="/users")

@router.post("/sign-up" , status_code=201)
def user_sign_up_handler(request : SignUpRequest  ,
                         user_service : UserService = Depends(),
                         user_repo : UserRepository = Depends()
                         ) -> UserShema:
    
    hashed_password : str = user_service.hash_password(
        plain_password=request.password
    )
    
    # 3. User(username , password) => User 객체 생성
    user : User = User.create(
        id = request.id,
        username=request.username,
        hashed_password = hashed_password
    )
    
    # 4. user -> db에 저장
    user : User = user_repo.save_user(user = user)
    
    
    return UserShema.model_validate(user)

@router.post("/log-in")
def user_log_in_handler(
    request : Login_by_user,
    user_service : UserService = Depends(),
    user_repo : UserRepository = Depends()
    
):

    user : User | None = user_repo.get_User_by_username(
        username=request.username
    )
    
    #if user not null 과 if not user 에 차이 
    
    if user is None:
        raise HTTPException(status_code=404 , detail="User not found")
    
    
    #3 user.password , reuqest.password -> bcrypt checkow
    verified = user_service.verify_password(
        plain_password=request.password
        ,hashed_password=user.password
                                )
    
    if not verified:
        raise HTTPException(status_code=401 , detail="Not Authorized")
    
    #4 create jwt
    
    access_token : str = user_service.create_jwt(username=request.username)
    
    return JWTResponse(access_token=access_token)