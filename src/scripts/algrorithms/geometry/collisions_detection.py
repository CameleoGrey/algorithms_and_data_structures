


import heapq
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle

class Particle:
    def __init__(self, x, y, vx, vy, radius, mass, id_num):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.mass = mass
        self.id = id_num
        self.count = 0  # collision count
    
    def move(self, dt):
        """Move the particle for dt time units"""
        self.x += self.vx * dt
        self.y += self.vy * dt
    
    def time_to_hit(self, other):
        """Calculate time until collision with another particle, or infinity if no collision"""
        if self == other:
            return float('inf')
        
        dx = other.x - self.x
        dy = other.y - self.y
        dvx = other.vx - self.vx
        dvy = other.vy - self.vy
        
        dvdr = dx * dvx + dy * dvy
        if dvdr >= 0:
            return float('inf')
        
        dvdv = dvx * dvx + dvy * dvy
        drdr = dx * dx + dy * dy
        sigma = self.radius + other.radius
        d = (dvdr * dvdr) - dvdv * (drdr - sigma * sigma)
        
        if d < 0:
            return float('inf')
        
        return -(dvdr + math.sqrt(d)) / dvdv
    
    def time_to_hit_vertical_wall(self, box_width):
        """Time until collision with a vertical wall"""
        if self.vx > 0:
            return (box_width - self.x - self.radius) / self.vx
        elif self.vx < 0:
            return (self.radius - self.x) / self.vx
        else:
            return float('inf')
    
    def time_to_hit_horizontal_wall(self, box_height):
        """Time until collision with a horizontal wall"""
        if self.vy > 0:
            return (box_height - self.y - self.radius) / self.vy
        elif self.vy < 0:
            return (self.radius - self.y) / self.vy
        else:
            return float('inf')
    
    def bounce_off(self, other):
        """Update velocities after elastic collision with another particle"""
        dx = other.x - self.x
        dy = other.y - self.y
        dvx = other.vx - self.vx
        dvy = other.vy - self.vy
        dvdr = dx * dvx + dy * dvy
        dist = self.radius + other.radius
        
        # Calculate impulse
        J = 2 * self.mass * other.mass * dvdr / ((self.mass + other.mass) * dist)
        Jx = J * dx / dist
        Jy = J * dy / dist
        
        # Update velocities
        self.vx += Jx / self.mass
        self.vy += Jy / self.mass
        other.vx -= Jx / other.mass
        other.vy -= Jy / other.mass
        
        # Update collision counts
        self.count += 1
        other.count += 1
    
    def bounce_off_vertical_wall(self):
        """Reverse x-velocity when hitting a vertical wall"""
        self.vx = -self.vx
        self.count += 1
    
    def bounce_off_horizontal_wall(self):
        """Reverse y-velocity when hitting a horizontal wall"""
        self.vy = -self.vy
        self.count += 1
    
    def kinetic_energy(self):
        """Calculate kinetic energy of the particle"""
        return 0.5 * self.mass * (self.vx**2 + self.vy**2)

class Event:
    def __init__(self, time, a, b):
        self.time = time  # time of event
        self.a = a        # first particle involved (None if wall)
        self.b = b        # second particle involved (None if wall or single particle)
        self.count_a = a.count if a is not None else -1
        self.count_b = b.count if b is not None else -1
    
    def __lt__(self, other):
        """Compare events by time"""
        return self.time < other.time
    
    def is_valid(self):
        """Check if this event is still valid (no intervening collisions)"""
        if self.a is not None and self.a.count != self.count_a:
            return False
        if self.b is not None and self.b.count != self.count_b:
            return False
        return True

class ParticleSimulation:
    def __init__(self, width, height, particles):
        self.width = width
        self.height = height
        self.particles = particles
        self.time = 0.0
        self.pq = []  # priority queue for events
        self.history = []  # for animation
    
    def predict_collisions(self, a):
        """Predict all future collisions for particle a and add to priority queue"""
        if a is None:
            return
        
        # Particle-particle collisions
        for particle in self.particles:
            if particle == a:
                continue
            dt = a.time_to_hit(particle)
            if dt != float('inf'):
                heapq.heappush(self.pq, Event(self.time + dt, a, particle))
        
        # Wall collisions
        dt = a.time_to_hit_vertical_wall(self.width)
        if dt != float('inf'):
            heapq.heappush(self.pq, Event(self.time + dt, a, None))
        
        dt = a.time_to_hit_horizontal_wall(self.height)
        if dt != float('inf'):
            heapq.heappush(self.pq, Event(self.time + dt, None, a))
    
    def initialize_events(self):
        """Initialize the priority queue with all possible events"""
        self.pq = []
        for i in range(len(self.particles)):
            self.predict_collisions(self.particles[i])
    
    def simulate(self, duration, animate=False, save_history=False):
        """Run the simulation for the given duration"""
        self.initialize_events()
        self.time = 0.0
        
        if save_history:
            self.history = [self.get_state()]
        
        while self.time < duration:
            if not self.pq:
                break
            
            event = heapq.heappop(self.pq)
            
            if not event.is_valid():
                continue
            
            # Move all particles to the time of the event
            dt = event.time - self.time
            for p in self.particles:
                p.move(dt)
            self.time = event.time
            
            # Process the event
            a = event.a
            b = event.b
            
            if a is not None and b is not None:
                a.bounce_off(b)
            elif a is not None and b is None:
                a.bounce_off_vertical_wall()
            elif a is None and b is not None:
                b.bounce_off_horizontal_wall()
            
            # Update predictions for the particles involved
            self.predict_collisions(a)
            self.predict_collisions(b)
            
            if save_history:
                self.history.append(self.get_state())
        
        # Move particles to the end time if simulation ended early
        if self.time < duration:
            dt = duration - self.time
            for p in self.particles:
                p.move(dt)
            self.time = duration
            
            if save_history:
                self.history.append(self.get_state())
    
    def get_state(self):
        """Get current state of all particles for visualization"""
        return [(p.x, p.y, p.vx, p.vy, p.radius) for p in self.particles]
    
    def total_kinetic_energy(self):
        """Calculate total kinetic energy of the system"""
        return sum(p.kinetic_energy() for p in self.particles)
    
    def animate_simulation(self, frames=None, interval=50):
        """Create an animation of the simulation"""
        if not self.history:
            raise ValueError("No history saved. Run simulate with save_history=True first.")
        
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        ax.set_aspect('equal')
        ax.add_patch(Rectangle((0, 0), self.width, self.height, fill=False))
        
        # Create circles for particles
        circles = []
        for _ in self.particles:
            circle = plt.Circle((0, 0), 0, color='blue')
            ax.add_patch(circle)
            circles.append(circle)
        
        if frames is None:
            frames = len(self.history)
        
        def update(frame):
            state = self.history[frame * len(self.history) // frames]
            for i, (x, y, _, _, radius) in enumerate(state):
                circles[i].center = (x, y)
                circles[i].radius = radius
            return circles
        
        anim = FuncAnimation(fig, update, frames=frames, interval=interval, blit=True)
        plt.close()
        return anim

def create_random_particles(n, width, height, min_radius=0.01, max_radius=0.05):
    """Create n random particles within the given bounds"""
    particles = []
    for i in range(n):
        radius = np.random.uniform(min_radius, max_radius)
        x = np.random.uniform(radius, width - radius)
        y = np.random.uniform(radius, height - radius)
        
        # Random velocity with magnitude inversely proportional to radius
        speed = np.random.uniform(0.01, 0.1) / radius
        angle = np.random.uniform(0, 2 * np.pi)
        vx = speed * np.cos(angle)
        vy = speed * np.sin(angle)
        
        # Mass proportional to area (radius squared)
        mass = radius ** 2
        
        particles.append(Particle(x, y, vx, vy, radius, mass, i))
    return particles

# Example usage
if __name__ == "__main__":

    # Parameters
    width, height = 1.0, 1.0
    num_particles = 20
    simulation_duration = 10.0
    
    # Create particles and simulation
    particles = create_random_particles(num_particles, width, height)
    sim = ParticleSimulation(width, height, particles)
    
    # Run simulation and save history for animation
    sim.simulate(simulation_duration, save_history=True)
    
    # Display total kinetic energy (should be conserved)
    print(f"Total kinetic energy: {sim.total_kinetic_energy():.4f}")
    
    # Create and display animation
    anim = sim.animate_simulation(frames=600, interval=50)

    with open("./collision_detection_animation.html", "w") as animation_file:
        animation_file.write(anim.to_jshtml())