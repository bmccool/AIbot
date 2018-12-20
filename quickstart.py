import retro
import time
import threading

def sounder(sound):
	print(sound)

def playSound(sound):
	t = threading.Thread(target=sounder, args=(sound,))
	t.start()

class FpsLock():


    def __init__(self, fps):
    	self.frame = 0
    	self.fps = fps
    	self.start = None

    def tick(self):
    	if self.start is None:
    		self.start = time.perf_counter()
    	self.frame += 1
    	target = self.frame / self.fps
    	passed = time.perf_counter() - self.start
    	differ = target - passed
    	if differ < 0:
    		return True
    	time.sleep(differ)
    	return False

    def lockedStep(self, env):
    	if self.tick():
    		print("Missed on frame {}!".format(self.frame))
    	return env.step(env.action_space.sample())


def main():
    env = retro.make(game='SuperMarioBros-Nes')
    obs = env.reset()
    fpsLock = FpsLock(60)
    while True:
        #obs, rew, done, info = env.step(env.action_space.sample())
        obs, rew, done, info = fpsLock.lockedStep(env)
        playSound(env.em.get_audio())
        env.render()
        if done:
            obs = env.reset()


if __name__ == '__main__':
    main()