/*
API configuration

The backend's base URL, shared by every file in src/api.

It can be set with VITE_API_BASE_URL in frontend/.env
(ignored by git), e.g.:

    VITE_API_BASE_URL=http://localhost:8000

When it is not set, the local backend address is used.
Vite reads .env when the dev server starts, so restart
`npm run dev` after changing it.
*/

export const API_BASE_URL: string =
    import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";
