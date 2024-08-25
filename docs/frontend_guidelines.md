# Frontend Coding Guidelines

## Angular
- Use Angular's standalone components.
- Organize components, services, and models into appropriate directories.
- Use Angular's built-in pipes for data transformation in templates.
- Implement proper error handling and display user-friendly messages.
- Use Angular's HttpClient for API calls.

## Testing
- Write unit tests for components and services.
- Implement integration tests for critical user flows.
- Use Angular's TestBed for component testing.

## Angular Material
- Use Angular Material components for consistent UI elements across the application.
- Import only the necessary Material modules in each component to optimize bundle size.
- Customize Material themes in a separate `custom-theme.scss` file.
- Use Material's typography system for consistent text styling.
- Leverage Material's responsive layout components (e.g., mat-grid-list) for adaptive designs.

## Styling
- Use SCSS for styling components.
- Follow a consistent naming convention for CSS classes (e.g., BEM methodology).
- Utilize Angular's component-specific styling to avoid global style conflicts.
- When customizing Material components, use Angular Material's theming system.

## Performance
- Lazy load Angular Material modules when possible to reduce initial bundle size.
- Implement lazy loading for modules when appropriate.
- Use Angular's OnPush change detection strategy for performance optimization where possible.
- Optimize asset loading (images, fonts, etc.) for faster initial page loads.

## Accessibility
- Follow WCAG 2.1 guidelines for accessibility.
- Use semantic HTML elements and ARIA attributes where necessary.
- Ensure keyboard navigation is possible for all interactive elements.

## State Management
- For complex state management, consider using NgRx or a similar state management library.
- For simpler cases, utilize Angular services and RxJS for state management.

## Code Organization
- Keep components small and focused on a single responsibility.
- Use smart/dumb component pattern (container/presentational components).
- Implement proper error handling and display user-friendly messages.
