
all: userDocs

userDocs:
	cd iosity4_0_5; ./precompiledir.pl -i ../userSrc/ -o ../userDoc/; \
        cd ../userDoc; cp ../userSrc/*.html .; \
        mkdir images; cp ../userSrc/images/* images/.

clean:
	rm -f userDoc/*.html; rm -rf userDoc/images

