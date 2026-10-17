# R3F Platformer (WIP)

It's in progress! 🚧

A 2D platformer game built with React Three Fiber (R3F) and integrated with LDTK (Level Designer Toolkit) for level design and physics using Rapier.

## 🛠 TODO

- ~~(LDTK) Add IntGrid Layer Renderer~~
- (LDTK) Add AutoLayer Renderer
- Multiple Levels & Transitions
- ~~Animation System~~
- Audio System
- Dialogue System
- ~~Lighting & Shadows~~
- Particle Effects
- Save/Load System
- Cutscenes
- Power-ups & Items
- Enemy AI (Decision Trees, Navigation)

## 🎮 Features

- **React Three Fiber**: 3D graphics rendering with React declarative approach
- **LDTK Integration**: Level design using LDTK editor with custom renderers
- **Physics**: Realistic physics simulation using Rapier physics engine
- **TypeScript**: Full TypeScript support for type safety
- **Component-based Architecture**: Modular and reusable game components
- **Entity System**: Custom entity rendering system for game objects
- **Tile-based Levels**: Support for tile-based level design with collision detection

## 🚀 Tech Stack

- **React 19** - UI framework
- **React Three Fiber** - React renderer for Three.js
- **React Three Drei** - Useful helpers for R3F
- **React Three Rapier** - Physics integration
- **Three.js** - 3D graphics library
- **LDTK** - Level Designer Toolkit integration
- **TypeScript** - Type-safe development
- **Vite** - Fast build tool and dev server
- **pnpm** - Package manager

## 📁 Project Structure

```
src/
├── Game.tsx                    # Main game component
├── App.tsx                     # Application entry point
├── common/
│   └── ldtk/                   # LDTK integration modules
│       ├── components/
│       │   ├── LdtkMap.tsx     # LDTK map renderer
│       │   ├── layers/         # Layer rendering components
│       │   └── tiles/          # Tile rendering components
│       ├── models/
│       │   └── LdtkTypes.ts    # LDTK type definitions
│       └── utils/              # Utility functions
public/
└── assets/
    └── ldtk/                   # LDTK project files and tilesets
```

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd r3f-platformer
   ```

2. **Install dependencies**
   ```bash
   pnpm install
   ```

3. **Start development server**
   ```bash
   pnpm dev
   ```

4. **Open your browser**
   Navigate to `http://localhost:8080`

## 🎯 Development

### Available Scripts

- `pnpm dev` - Start development server
- `pnpm build` - Build for production
- `pnpm preview` - Preview production build

### LDTK Integration

The project includes a custom LDTK integration that allows you to:

- Load LDTK project files (`.ldtk`)
- Render tiles with collision detection
- Place entities with custom renderers
- Support for multiple layers and levels

#### Adding New Entities

Define entity renderers in the `entityRendererMap`:

```tsx
entityRendererMap={{
  "PlayerStart": ({entity, layer, layerPxOffsets, layerPxDimensions}) => {
    // Custom entity rendering logic
    return <YourEntityComponent />
  }
}}
```

#### Adding New Tiles

Define tile renderers in the `tileRendererMap`:

```tsx
tileRendererMap={{
  "RECT": (props) => (
    <>
      <TileSprite {...props}/>
      <TileRectCollider {...props}/>
    </>
  )
}}
```

### Physics System

The game uses Rapier physics engine through `@react-three/rapier`:

- Rigid bodies for physics objects
- Collision detection for tiles and entities
- Debug mode available during development

## 🎨 Level Design

1. **Use LDTK Editor** to create levels
2. **Place your `.ldtk` file** in `public/assets/ldtk/`
3. **Configure tile renderers** for your tilesets
4. **Add entity renderers** for game objects

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add appropriate types and tests
5. Submit a pull request

## 🔧 Configuration

### TypeScript

The project uses multiple TypeScript configurations:
- `tsconfig.json` - Base configuration
- `tsconfig.app.json` - Application-specific settings
- `tsconfig.node.json` - Node.js build tools

### Vite

Custom Vite configuration includes:
- Path aliases (`@` points to `src/`)
- Development server on port 8080
- React plugin for fast refresh

## 📄 License

[Add your license here]

## 🤝 Acknowledgments

- LDTK for the excellent level editor
- React Three Fiber community
- Rapier physics engine
