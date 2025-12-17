**Introduction**
- **Project:** Frontend application (React + TypeScript)

**Prerequisites**
- **Node.js:** LTS version (recommended >= 16)
- **Package manager:** `npm` or `yarn`

**Setup**
- **Install dependencies:** `npm install` or `yarn`
- **Environment variables:** create a `.env` file in the project root with your Firebase keys (example below)

**Firebase environment variables**
- **Expected keys:** defined in `src/services/firebase.ts`
- **Example `.env`:**

```
REACT_APP_API_KEY=your_api_key
REACT_APP_AUTH_DOMAIN=your_auth_domain
REACT_APP_DATABASE_URL=your_database_url
REACT_APP_PROJECT_ID=your_project_id
REACT_APP_STORAGE_BUCKET=your_storage_bucket
REACT_APP_MESSAGING_SENDER_ID=your_messaging_sender_id
REACT_APP_APP_ID=your_app_id
```

**Useful scripts**
- `start`: runs the development server (`npm start`)

**Project structure (summary)**
- `package.json`: dependencies and scripts
- `tsconfig.json`: TypeScript configuration
- `public/`: static files, including `index.html`
- `src/`: main source code
  - `src/App.tsx`: main application component ([src/App.tsx](src/App.tsx))
  - `src/index.tsx`: React bootstrap ([src/index.tsx](src/index.tsx))
  - `src/services/firebase.ts`: Firebase configuration and exports ([src/services/firebase.ts](src/services/firebase.ts))
  - `src/pages/`: main pages (e.g. [src/pages/Home.tsx](src/pages/Home.tsx), [src/pages/Room.tsx](src/pages/Room.tsx))
  - `src/components/`: reusable components (e.g. `Button`, `Popup`, `RoomCode`)
  - `src/hooks/`: custom hooks (`useAuth`, `useRoom`)
  - `src/contexts/`: React contexts (e.g. `AuthContext`)
  - `src/styles/`: global and component SCSS/CSS files

**Deployment notes**
- The `build/` folder (produced by `npm run build`) contains the files ready to deploy.
- Serve the static build with your hosting provider (Netlify, Vercel, Firebase Hosting, etc.).
