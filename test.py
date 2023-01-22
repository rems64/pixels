import pygame

vec2 = pygame.Vector2
vec3 = pygame.Vector3

pygame.init()
size = vec2(1280, 720)
ratio = size.y/size.x
print(ratio)

definition = 64

drawing_surface = pygame.surface.Surface(vec2(definition/ratio, definition))
screen = pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.RESIZABLE)

def load_image(path):
    return pygame.image.load(path)

position = vec2(0, 0)

img = load_image("player.png")
m1 = load_image("metal_beam_h1.png")
m2 = load_image("metal_beam_h2.png")
m3 = load_image("metal_beam_h3.png")

clock = pygame.time.Clock()

carryOn = True
while carryOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False
        if event.type == pygame.VIDEORESIZE:
            print("Resize")
            pygame.display.update()
            size = vec2(event.dict["size"][0], event.dict["size"][1])
            ratio = size.y/size.x
            # drawing_surface = pygame.surface.Surface(vec2(int(definition/ratio), int(definition)))

    
    fac = 1
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:  position+=vec2(-1,  0)*fac
    if keys[pygame.K_RIGHT]: position+=vec2( 1,  0)*fac
    if keys[pygame.K_UP]:    position+=vec2( 0, -1)*fac
    if keys[pygame.K_DOWN]:  position+=vec2( 0,  1)*fac
    
    drawing_surface.fill(vec3())

    drawing_surface.blit(m1, vec2(30, 20))
    drawing_surface.blit(m2, vec2(30+16, 20))
    drawing_surface.blit(m3, vec2(30+2*16, 20))

    drawing_surface.blit(img, position)
    if abs(ratio-drawing_surface.get_size()[1]/drawing_surface.get_size()[0])>0.02:
        print("Non square final pixels, recalculating drawing_surface")
        # ratio = size.y/size.x
        drawing_surface = pygame.surface.Surface(vec2(int(definition/ratio), int(definition)))
    
    pygame.transform.scale(drawing_surface, size, screen)

    pygame.display.flip()

    clock.tick(60)