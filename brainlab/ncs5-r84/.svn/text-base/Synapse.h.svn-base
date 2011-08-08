#ifndef SYNAPSE_H
#define SYNAPSE_H

#include "Global.h"
#include <math.h>
#include <stdlib.h>
#include <stdio.h>

#include "InitStruct.h"
#include "Compartment.h"
#include "SynapseDef.h"
#include "Random.h"
#include "defines.h"
#include "Augmentation.h"

#define EPSILON 0.0001

using namespace std;

//@Include: SynapseDef.h
//@Include: Augmentation.h

/**
 * The Synapse object is the receiving end of a connection between cells.
 * Owned by some compartment within the cell, it is called to do
 * processing whenever it receives a message from the sending side.  That
 * processing includes placing it on the compartment's active list, where it
 * contributes to the compartment voltage as specified by the PSG template &
 * factors, and does learning &c.
 */
class Synapse
{
public:
          ///ID of this Synapse within the compartment (0..n)
  //int SynapseID;
          ///Synapse definition info for this synapse
  SynapseDef *SynDef;
          ///Pointer to the Compartment that owns this synapse
  Compartment *Cmp;
          ///TimeStep when this synapse last had a spike
  int PreviousSpikeTime;
          ///If synaptic augmentation is activated, allocate an augmentation object
  Augmentation *synAugmentation;
          ///Counter to record the times of positive learning for one spike
  int counterPosLearning; 
          ///Counter to record how many times this synapse has received negative learning
  int counterNegLearning;
          ///The maximum number of times negative learning can be applied to this synapse
  int limitNegLearning;
          ///The maximum number of times positive learning can be applied to this synapse
  int limitPosLearning;
          ///Modulation factor for positive learning 
  double ModPosLearning;
          ///Modulation factor for negative learning
  double ModNegLearning;

#ifdef USE_FLOAT
  float SynReversal;
  float MaxG;
 
  float USE;               
  float RSE_New; 
  float RSE_Old;
  float USE_New;     
  float USE_Old;
  
  float Tau_Depr;          
  float Tau_Facil;         
#else
  double SynReversal;
  double MaxG;
 
  double USE;               
  double RSE_New; 
  double RSE_Old;
  double USE_New;     
  double USE_Old;
  
  double Tau_Depr;          
  double Tau_Facil;         
#endif

// functions
  
  /**
   * Default constructor
   */
  Synapse ();

  /**
   * Primary Constructor used when building brain from input file.
   *
   * @param SYNDEF pointer to auxillary synase data. Learning, PSG, FD.
   * @param CMP pointer to parent Compartment object
   * @param RN pointer to random number generator
   */
  Synapse (SynapseDef *SYNDEF, Compartment *CMP, Random *RN);

  /**
   * Destructor, notifies memory tracker that resources have been freed
   */
  ~Synapse ();           

  /**
   * Receive an incoming spike from another cell.  Called by the parent cmp
   * when it receives a SPIKE message.  Computes a modification factor for the
   * generic spike template according to various internal values and updates
   * spike time histories.
   *
   * @param TimeStep iteration of Brain::DoThink
   */
  void ReceiveMsg (int TimeStep);

  /**
   * Whenever the parent cmp fires, this function checks to see if the
   * synapse received an incoming spike message within the positive learning
   * window.  In other words, whether this synapse contributed to the firing.
   * If so, the USE value is modified according to the value in the learning
   * table for the interval.  This function is only called if the synapse
   * was declared as using positive learning in the input file
   *
   * @param TimeStep iteration of Brain::DoThink
   */
  void DoPositiveLearning (int TimeStep);

  /**
   * Whenever the presynaptic cell fires and this synapse updates (via member
   * function ReceiveMsg), this function checks to see if the postsynaptic cell
   * (i.e. the parent cmp to this object) has spiked recently and this new 
   * synapse arrival has fallen in the negative learning window.
   * In other words, whether this synapse failed to contributed to the firing.
   * If so, the USE value is modified according to the value in the learning
   * table for the interval.  This function is only called if the synapse
   * was declared as using negative learning in the input file
   *
   * @param TimeStep iteration of Brain::DoThink
   */
  void DoNegativeLearning (int TimeStep);

  /**
   * Since negative learning can only be applied to a synapse for a limited number
   * of times (default=1), there needs to be a method for letting the synapse know
   * when it can receive the negative learning again.  This function resets the counter
   * and should be called by an external entity that knows when is a good time for resetting
   * the counter.  FOr now, that external entity is the post-synaptic cell that owns this
   * synapse, and it resets it when it fires (thus creating a new negative learning window)
   *
   * @param TImeStep The current interation of Brain::DoThink
   */
  void ResetNegativeLearningCounter( int TimeStep );

  /**
   * Write Synaptic data to a file.  Called by Compartment object.
   *
   * @param out File stream where data is sent
   * @return number of bytes written
   */
  int Save( FILE *out );

  /**
   * Load Synaptic data from a file. Called by Compartment object.
   *
   * @param in File stream where data comes from
   * @param nothing character string to make pointers use. Will hopefully be phased out
   */
  void Load( FILE *in, char *nothing );

  /**
   * Function to compute the ID of this synapse by calculating the offset from the
   * front of the array. This allows memory to be saved since a separate variable for
   * the id does not need to be kept.
   */
  int getID();
};

//---------------------------------------------------------------------------
// Inline functions
//---------------------------------------------------------------------------

inline void Synapse::ResetNegativeLearningCounter( int TimeStep )
{
    counterNegLearning = 0;
}

#endif

