# Capstone Completion Checklist

## Implemented
- React/Vite frontend
- Express/Node REST API
- MongoDB data models
- JWT authentication
- Scholarship discovery/search
- Scholarship application tracking API
- Document upload/list API
- FastAPI recommendation service
- Admin statistics API
- Seed scholarship data
- Dockerfiles and docker-compose
- Backend smoke tests
- Responsive UI

## Run locally
1. `docker compose up --build`
2. Open `http://localhost:5173`
3. For sample data: `cd backend && npm install && npm run seed`
4. Backend tests: `cd backend && npm test`

## Production notes
Set strong `JWT_SECRET`, production MongoDB credentials, `CLIENT_URL`, and `ML_SERVICE_URL` before deployment. File storage should use object storage in production rather than the local uploads directory.
