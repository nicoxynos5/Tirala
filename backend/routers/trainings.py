from fastapi import APIRouter, HTTPException, Depends, status
from repository.training import TrainingRepository
from schemas.user_schema import UserBase
from schemas.training_schema import Training25Shots
from graphs.trainings import generate_graphs_per_position
from deps.user_deps import get_current_user
from fastapi.responses import JSONResponse


router = APIRouter(
    prefix='/trainings',
)


@router.get('', summary="Get all training plans", status_code=status.HTTP_200_OK)
async def get_general_trainings():
    training_repo = TrainingRepository()
    try:
        training_plans = training_repo.get_all_training()
        return training_plans
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                             detail='An error occurred while getting the training_plans')


@router.post('/25_shots', summary="Create a new training session",
            status_code=status.HTTP_201_CREATED)
async def create_training_25_shots(
                                data_session: Training25Shots,
                                user: UserBase = Depends(get_current_user)
                            ):
    training_repo = TrainingRepository()
    try:
        data_session.user_id = user.id # le asigno el id del user obtenido de Depend
        training_repo.create_training_25_shots(data_session)
        return {'message': 'Training created'}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                             detail='An error occurred while creating the training')
    

@router.get('/25_shots',
            summary="Get statistics for the 25-shot training sessions",
            status_code=status.HTTP_200_OK)
async def get_sessions_25_shots(user: UserBase = Depends(get_current_user)):
    training_repo = TrainingRepository()
    try:
        sessions = training_repo.get_sessions_25_shots(user.id)
        percentages = training_repo.get_percentages_25_shots(user.id)
        graphs = generate_graphs_per_position(sessions)

        if not sessions or not percentages or not graphs:
            return JSONResponse(content={"message": "No training sessions found",
                                         "trainings": [], "percentages": [], "graphs": []})

        return JSONResponse(content={"trainings": sessions,
                                     "percentages": percentages,
                                     "graphs": graphs})
            
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='An error occurred while getting the training sessions')
    