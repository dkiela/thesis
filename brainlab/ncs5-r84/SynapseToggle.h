/*
 *  SynapseToggle.h
 *  ncs5
 *
 *  Created by James King on 4/18/07.
 *  Copyright 2007 __MyCompanyName__. All rights reserved.
 *
 */

#ifndef SYNAPSE_TOGGLE_H
#define SYNAPSE_TOGGLE_H

class SynapseDef;

/**
 * Helper object to keep track of Synapses that will be toggling Hebbian status
 * on and off
 */
class SynapseToggle
{
    private:
        /**
         * The SynapseDef object that will be modified
         */
        SynapseDef* synapseDef;
        
        /**
         * When this toggle should occur (seconds)
         */
        double time;
        
        /**
         * Flag to indicate if the synapse should use what it was declared with (1) or turn off (0)
         */
        int mode;
    
    public:
        /**
         * Create a SynapseToggle object that affects a specified SynapseDef object at a given time,
         * setting the learning to the given mode 
         *
         * @param pDef Pointer to SynapseDef that will be affected when by the SynapseToggle
         * @param pTime Simulation time (in seconds) when the toggle will be applied
         * @param pMode Whether the Learning will go to NONE (0) or go to what the Def was declared with (1)
         */
        SynapseToggle( SynapseDef *pDef, double pTime, int pMode );
        
        /**
         * Less than operator to allow priority_queue maintenence.  Looks at
         * double time to give lowest times higher priority
         */
        bool operator<( const SynapseToggle &RHS ) const;
        
        /**
         * Get the time when this toggle should be applied
         *
         * @return Time of toggle application
         */
        double getTime() const;
        
        /**
         * Retrieve reference to the SynapseDef that is affected by the toggle
         *
         * @return Pointer to SynapseDef object
         */
        SynapseDef* getSynapseDef() const;
        
        /**
         * Get the mode for the toggle
         *
         * @return Toggle mode - 0 for NONE, 1 for what the SynapseDef was declared with
         */
        int getMode() const;
};

//----------------------------------------------------------------------------------
// Inline functions
//----------------------------------------------------------------------------------

inline bool SynapseToggle::operator<( const SynapseToggle &RHS ) const
{
    //this is using greater than on purpose.  It flips the priority queue's behavior
    return time > RHS.time;
}

//----------------------------------------------------------------------------------

inline double SynapseToggle::getTime() const
{
    return time;
}

//----------------------------------------------------------------------------------

inline SynapseDef* SynapseToggle::getSynapseDef() const
{
    return synapseDef;
}

//----------------------------------------------------------------------------------

inline int SynapseToggle::getMode() const
{
    return mode;
}

#endif
